# pylint: disable=missing-docstring
# pylint: disable=import-error

import mimetypes
import json
from google.cloud import storage

import config as cfg

import six


def upload_to_gcloud():
    link_map = dict()
    f = open('ingredient_images.json', 'r')
    ingredient_img_map_json = json.load(f)
    f.close()
    for ing_id in ingredient_img_map_json:
        img_file = open('', 'r')
        img_file.close()
        return
    """
    GET_ALL_ING_IDS
    FOR EACH ING_ID:
        LOAD FILE
        URL = UPLOAD TO GCLOUD
        NEW_LINKS_MAP[IND_ID] = URL

    FOR EACH ING_ID IN NEW_LINKS_MAP:
        UPDATE_IMAGE
        CALL NOELS SCRIPPTTT???
    """

def upload_to_bucket(file_stream, filename):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    client = storage.Client(project=cfg.PROJECT_ID)
    bucket = client.bucket(cfg.CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=mimetypes.guess_type(filename))

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

if __name__ == "__main__":
    upload_to_gcloud()
