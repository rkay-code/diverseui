import os
import boto
import boto.s3
from boto.s3.key import Key
import requests
import uuid


# http://stackoverflow.com/a/42493144
def upload_url_to_s3(image_url):
    image_res = requests.get(image_url, stream=True)
    image = image_res.raw
    image_data = image.read()

    fname = str(uuid.uuid4())

    conn = boto.connect_s3(os.environ['AWS_ACCESS_KEY_ID_DIVERSEUI'],
                           os.environ['AWS_SECRET_KEY_DIVERSEUI'])
    bucket = conn.get_bucket('static.diverseui.com')

    k = Key(bucket, fname)
    k.set_contents_from_string(image_data)
    k.make_public()

    return 'https://static.diverseui.com/{}'.format(fname)
