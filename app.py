import os

from flask import Flask, render_template, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgresql://localhost/diverseui'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    BASIC_AUTH_USERNAME=os.environ.get('BASIC_AUTH_USERNAME', 'dev'),
    BASIC_AUTH_PASSWORD=os.environ.get('BASIC_AUTH_PASSWORD', 'secret')
))

db = SQLAlchemy(app)

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), unique=True)
    gender = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, url, gender):
        self.url = url
        self.gender = gender

    def __repr__(self):
        return '<Image url={0} gender={1}>'.format(self.url, self.gender)

    def to_json(self):
        return {
            'id': self.id,
            'url': self.url,
            'gender': self.gender,
            'created_at': self.created_at
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

class ImageView(BasicAuthModelView):
    form_excluded_columns = ['created_at']

admin = Admin(app, index_view=BasicAuthAdminView(), name='Diverse UI', template_mode='bootstrap3')
admin.add_view(ImageView(Image, db.session))

@app.route('/', methods=['GET'])
def index():
    images = Image.query.order_by('random()').all()

    return render_template('index.html',
                           images=[image.to_json() for image in images])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
