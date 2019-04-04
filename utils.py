import os
import boto
import boto.s3
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat
import requests
import uuid


# http://stackoverflow.com/a/42493144
def upload_url_to_s3(image_url):
    image_res = requests.get(image_url, stream=True)
    image = image_res.raw
    image_data = image.read()

    fname = str(uuid.uuid4())

    conn = boto.connect_s3(
        aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID_DIVERSEUI'],
        aws_secret_access_key = os.environ['AWS_SECRET_KEY_DIVERSEUI'],
        calling_format = OrdinaryCallingFormat(),
    )
    bucket = conn.get_bucket('static.diverseui.com')

    k = Key(bucket, fname)
    k.set_contents_from_string(image_data)
    k.make_public()

    return 'https://static.diverseui.com/{}'.format(fname)
