import os
import boto3
import requests
import uuid


def upload_url_to_s3(image_url):
    image = requests.get(image_url, stream=True)
    fname = str(uuid.uuid4())
    s3 = boto3.resource('s3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID_DIVERSEUI'],
        aws_secret_access_key=os.environ['AWS_SECRET_KEY_DIVERSEUI'],
    )
    bucket = s3.Bucket('static.diverseui.com')
    bucket.upload_fileobj(image.raw, fname, ExtraArgs={
        'ACL': 'public-read',
    })

    return 'https://static.diverseui.com/{}'.format(fname)
