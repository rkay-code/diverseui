# http://stackoverflow.com/a/42493144
def upload_url_to_s3(image_url):
    """
    req_for_image = requests.get(internet_image_url, stream=True)
    file_object_from_req = req_for_image.raw
    req_data = file_object_from_req.read()

    # Do the actual upload to s3
    s3.Bucket(bucket_name_to_upload_image_to).put_object(Key=s3_image_filename, Body=req_data)
    """
