import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgresql://localhost/diverseui'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True
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

@app.route('/', methods=['GET'])
def index():
    images = Image.query.order_by('random()').all()

    return render_template('index.html',
                           images=[image.to_json() for image in images])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
