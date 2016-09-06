#! /usr/bin/env python

from os import listdir, path, environ
import boto
import boto.s3
from boto.s3.key import Key

from app import db, Image

BUCKET = 'diverse-ui'

conn = boto.connect_s3(environ['AWS_ACCESS_KEY_ID_DIVERSEUI'],
                       environ['AWS_SECREY_KEY_DIVERSEUI'])
bucket = conn.get_bucket(BUCKET)

image_path = path.join(path.expanduser('~'), 'Dropbox', 'diverseui')

for p in listdir(image_path):
    if not p.startswith('.'):
        print('Uploading {}...'.format(p))

        # Upload to S3
        k = Key(bucket, 'faces/{}'.format(p))
        k.set_contents_from_filename(path.join(image_path, p))
        k.make_public()

        # Save to the db
        url = 'https://s3-us-west-2.amazonaws.com/{0}/faces/{1}'.format(BUCKET, p)
        gender = 'female' if p.startswith('female') else 'male'
        i = Image(url, gender)
        db.session.add(i)

db.session.commit()

print('Done.')
