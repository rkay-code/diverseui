import os
import uuid
import boto
import boto.s3
from boto.s3.key import Key
from flask import Flask, render_template, send_from_directory, request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
from flask_basicauth import BasicAuth
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro
from flask_compress import Compress

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL',
                                           'postgresql://localhost/diverseui'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    BASIC_AUTH_USERNAME=os.environ.get('BASIC_AUTH_USERNAME', 'dev'),
    BASIC_AUTH_PASSWORD=os.environ.get('BASIC_AUTH_PASSWORD', 'secret'),
    MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    TEMPLATES_AUTO_RELOAD=os.environ.get('TEMPLATES_RELOAD', 'True') == 'True'
))
app.secret_key = os.environ.get('SECRET_KEY', 'somethingsecret')

Compress(app)

db = SQLAlchemy(app)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), unique=True)
    email = db.Column(db.String())
    gender = db.Column(db.String())
    race = db.Column(db.String())
    status = db.Column(db.String(), nullable=False, server_default='pending')
    verification_url = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, url='', email='', gender='',
                 race='', verification_url=''):
        self.url = url
        self.email = email
        self.gender = gender
        self.race = race
        self.verification_url = verification_url

    def __repr__(self):
        return '<Image url={0} gender={1}>'.format(self.url, self.gender)

    def to_json(self):
        return {
            'url': self.url,
            'gender': self.gender,
        }

basic_auth = BasicAuth(app)


class BasicAuthModelView(ModelView):
    def is_accessible(self):
        return basic_auth.authenticate()

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()


class BasicAuthAdminView(AdminIndexView):
    def is_accessible(self):
        return basic_auth.authenticate()

    def inaccessible_callback(self, name, **kwargs):
        return basic_auth.challenge()

    @expose('/')
    def index(self):
        counts = {}
        counts['both'] = Image.query.count()
        counts['female'] = Image.query.filter_by(gender='female').count()
        counts['male'] = Image.query.filter_by(gender='male').count()
        counts['accepted'] = Image.query.filter_by(status='accepted').count()
        counts['pending'] = Image.query.filter_by(status='pending').count()
        return self.render('admin/index.html', counts=counts)


class ImageView(BasicAuthModelView):
    list_template = 'admin/model/object_list.html'
    form_excluded_columns = ['created_at', 'verification_url']
    page_size = 50
    column_filters = ('gender', 'status')
    column_formatters = dict(url=macro('render_url'))

admin = Admin(app,
              index_view=BasicAuthAdminView(),
              name='Diverse UI',
              template_mode='bootstrap3')
admin.add_view(ImageView(Image, db.session))


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico')


@app.route('/', methods=['GET'])
def index():
    images = Image.query\
        .filter_by(status='accepted')\
        .order_by(func.random())\
        .all()

    return render_template('index.html',
                           images=[image.to_json() for image in images])


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        fname = '{0}-{1}'.format(str(uuid.uuid4()),
                                 secure_filename(image.filename))

        conn = boto.connect_s3(os.environ['AWS_ACCESS_KEY_ID_DIVERSEUI'],
                               os.environ['AWS_SECREY_KEY_DIVERSEUI'])
        bucket = conn.get_bucket('diverse-ui')

        k = Key(bucket, 'faces/{}'.format(fname))
        k.set_contents_from_file(image)
        k.make_public()

        url = 'https://d3iw72m71ie81c.cloudfront.net/{}'.format(fname)
        email = request.form['email']
        gender = request.form['gender']
        race = request.form['race']
        verification_url = request.form['verification_url']

        i = Image(url, email, gender, race, verification_url)

        db.session.add(i)

        try:
            db.session.commit()
        except IntegrityError:
            return render_template('submit.html',
                                   submitted=False,
                                   fields=request.form)

        return render_template('submit.html', submitted=True, fields={})
    else:
        return render_template('submit.html', submitted=False, fields={})


@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template('submit.html', submitted=False, fields={}), 413

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
