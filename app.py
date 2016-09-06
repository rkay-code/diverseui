import os

from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL',
                                           'postgresql://localhost/diverseui'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    BASIC_AUTH_USERNAME=os.environ.get('BASIC_AUTH_USERNAME', 'dev'),
    BASIC_AUTH_PASSWORD=os.environ.get('BASIC_AUTH_PASSWORD', 'secret')
))
app.secret_key = os.environ.get('SECRET_KEY', 'somethingsecret')

db = SQLAlchemy(app)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), unique=True)
    gender = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, url='', gender=''):
        self.url = url
        self.gender = gender

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
        return self.render('admin/index.html', counts=counts)


class ImageView(BasicAuthModelView):
    form_excluded_columns = ['created_at']
    page_size = 50
    column_filters = ('gender', )

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
    images = Image.query.order_by('random()').all()

    return render_template('index.html',
                           images=[image.to_json() for image in images])


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return render_template('submit.html', submitted=True)
    else:
        return render_template('submit.html', submitted=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
