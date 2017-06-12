import os
import requests
import boto
import boto.s3
import boto.ses
from functools import wraps
from itertools import ifilter
from flask import Flask, render_template, send_from_directory, \
    request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy.sql.expression import func
from sqlalchemy.orm.attributes import get_history
from flask_basicauth import BasicAuth
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro
from flask_assets import Environment
from flask_cors import CORS
from flask_login import login_user, logout_user, login_required, \
    LoginManager, current_user

from track import log_fetch
from utils import upload_url_to_s3

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

CORS(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)


def bounce_user(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user and current_user.is_authenticated:
            return redirect(url_for('review'))
        return func(*args, **kwargs)
    return decorated_view


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.get(user_id)

    if user:
        user.is_authenticated = True

    return user

Environment(app)

db = SQLAlchemy(app)

TWEET_URL = ('https://twitter.com/intent/tweet?'
             'text=I%20just%20uploaded%20my%20'
             'photo%20to%20diverseui.com%21%20'
             'See%20if%20you%20can%20find%20me%20:)')

TEXT_BODY = ('Hello,\n\n'
             'Thanks for submitting your photo to Diverse UI! '
             'We wanted to let you know your photo is now live. '
             'Go check it out and see if you can find yourself :)'
             '\n\n- Renee\nwww.diverseui.com')

HTML_BODY = ('<p style="margin-top: 0;">Hello,</p>'
             '<p>Thanks for submitting your photo to Diverse UI! '
             'We wanted to let you know your photo is now live.</p> '
             '<p><a target="_blank" href="{}">Share on Twitter</a> '
             'and see if your friends can find you :)</p>'
             '<p style="margin-bottom: 0;">- Renee<br />'
             '<a target="_blank" href="http://www.diverseui.com">'
             'www.diverseui.com</a></p>').format(TWEET_URL)

FB_BASE_URL = 'https://graph.facebook.com/v2.8'
FB_CLIENT_ID = os.environ.get('FB_CLIENT_ID', '')
FB_REDIRECT_URI = os.environ.get('FB_REDIRECT_URI', '')
FB_SECRET = os.environ.get('FB_SECRET', '')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    gender = db.Column(db.String())
    picture = db.Column(db.String())
    email = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    image = db.relationship('Image',
                            uselist=False,
                            backref='user')

    is_active = True
    is_anonymous = False
    is_authenticated = False

    def __init__(self, fb_id='', first_name='', picture='',
                 last_name='', gender='', email=''):
        self.is_authenticated = True
        self.fb_id = fb_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.picture = picture
        self.email = email

    def get_id(self):
        return self.id


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    url = db.Column(db.String(), unique=True)
    email = db.Column(db.String())
    gender = db.Column(db.String())
    race = db.Column(db.String())
    second_race = db.Column(db.String())
    status = db.Column(db.String(), nullable=False, server_default='pending')
    verification_url = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, url='', email='', gender='', race='',
                 second_race='', verification_url='', user_id=''):
        self.url = url
        self.email = email
        self.gender = gender
        self.race = race
        self.second_race = second_race
        self.verification_url = verification_url

        if user_id:
            self.user_id = user_id

    def __repr__(self):
        return '<Image url={0} gender={1}>'.format(self.url, self.gender)

    @staticmethod
    def after_update(mapper, connection, target):
        status_history = get_history(target, 'status')
        email = target.email
        # If the image went from pending to accepted, send an email
        if status_history.has_changes() and\
                status_history.deleted[0] == 'pending' and\
                status_history.added[0] == 'accepted':
            conn = boto.ses.connect_to_region(
                'us-east-1',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID_DIVERSEUI'],
                aws_secret_access_key=os.environ['AWS_SECRET_KEY_DIVERSEUI'])
            conn.send_email(
                'Renee at Diverse UI <hello@diverseui.com>',
                'Thanks for submitting to Diverse UI!',
                None,
                [email],
                format='html',
                text_body=TEXT_BODY,
                html_body=HTML_BODY)

    def to_json(self):
        return {
            'url': self.url,
            'gender': self.gender,
        }

event.listen(Image, 'after_update', Image.after_update)

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
        counts['female'] = Image.query\
                                .filter_by(gender='female', status='accepted')\
                                .count()
        counts['male'] = Image.query\
                              .filter_by(gender='male', status='accepted')\
                              .count()
        counts['accepted'] = Image.query.filter_by(status='accepted').count()
        counts['pending'] = Image.query.filter_by(status='pending').count()
        return self.render('admin/index.html', counts=counts)


class ImageView(BasicAuthModelView):
    list_template = 'admin/model/object_list.html'
    form_excluded_columns = ['created_at', 'verification_url', 'user']
    page_size = 50
    column_exclude_list = ('user')
    column_filters = ('gender', 'status')
    column_formatters = dict(
        url=macro('render_url'),
        verification_url=macro('render_verification_url')
    )

admin = Admin(app,
              index_view=BasicAuthAdminView(),
              name='Diverse UI',
              template_mode='bootstrap3')
admin.add_view(ImageView(Image, db.session))


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico')


@app.route('/robots.txt', methods=['GET'])
def robotstxt():
    return send_from_directory(os.path.join(app.root_path, 'static', 'txt'),
                               'robots.txt')


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static', 'txt'),
                               'sitemap.xml')


@app.route('/', methods=['GET'])
def index():
    images = Image.query\
        .filter_by(status='accepted')\
        .order_by(func.random())\
        .all()

    status = next(ifilter(
        lambda s: request.args.get(s) is not None,
        ['submitted', 'removed']
    ), None)

    dismissed = request.cookies.get('dismissed') is not None

    return render_template('index.html',
                           images=[image.to_json() for image in images],
                           status=status,
                           dismissed=dismissed)


@app.route('/images', methods=['GET'])
def images():
    images = Image.query.filter(Image.status == 'accepted')

    gender = request.args.get('gender')
    if gender:
        images = images.filter(Image.gender == gender.lower())

    images = images.order_by(func.random())

    count = request.args.get('count', 0, type=int)
    if count > 0:
        images = images.limit(int(count))

    log_fetch(count=images.count(), gender=gender)

    images = images.all()

    return jsonify([image.to_json() for image in images])


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')


@app.route('/auth', methods=['GET'])
def auth():
    code = request.args.get('code')

    if code is None:
        return redirect(url_for('submit', _anchor='failure'))

    # Get access_token from Facebook
    auth = requests.get('%s/oauth/access_token' % FB_BASE_URL, params={
        'client_id': FB_CLIENT_ID,
        'redirect_uri': FB_REDIRECT_URI,
        'client_secret': FB_SECRET,
        'code': code
    })

    access_token = auth.json()['access_token']

    # Get necessary fields from Facebook
    me = requests.get('%s/me' % FB_BASE_URL, params={
        'access_token': access_token,
        'fields': (
            'id,email,first_name,last_name,'
            'gender,picture.height(500).width(500)'
        )
    })

    fields = me.json()
    fb_id = fields.pop('id')
    user = User.query.filter_by(fb_id=fb_id).first()

    picture = fields.pop('picture').get('data', {}).get('url')

    if user is None:
        user = User(fb_id=fb_id, picture=picture, **fields)
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for('review', _anchor='success'))


@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    user = current_user
    image = user.image or Image(user_id=user.id)

    if request.method == 'POST':
        action = request.form['action']

        if action == 'remove':
            db.session.delete(image)
            db.session.commit()
            logout_user()
            return redirect('/?removed')

        image.email = request.form['email']
        image.gender = request.form['gender']
        image.race = request.form['race']
        image.second_race = request.form['second_race']

        if image.status:
            db.session.commit()
            return render_template('review.html',
                                   updated=True,
                                   user=user,
                                   image=image)
        else:
            image.url = upload_url_to_s3(user.picture)

            db.session.add(image)
            db.session.commit()
            return redirect('/?submitted')

    return render_template('review.html',
                           updated=False,
                           user=user,
                           image=image)


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/submit', methods=['GET'])
@bounce_user
def submit():
    return render_template('submit.html',
                           client_id=FB_CLIENT_ID,
                           redirect_uri=FB_REDIRECT_URI)


@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template('submit.html', submitted=False, fields={}), 413

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
