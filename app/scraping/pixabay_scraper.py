# pylint: disable=missing-docstring
# pylint: disable=import-error

import mimetypes
import json
from google.cloud import storage

import config as cfg

import six


def upload_to_gcloud():
    link_map = dict()
    map_file = open('ingredient_images.json', 'r')
    ingredient_img_map_json = json.load(map_file)
    map_file.close()
    for ing_id in ingredient_img_map_json:
        fname = 'saved_ingredient_images/{}.jpg'.format(ing_id)
        img_file = open(fname, 'rb')
        url = upload_to_bucket(img_file, fname)
        print(url)
        img_file.close()

        link_map[str(ing_id)] = url

    with open('cloud_storage_ingredient_images_url.json', 'w') as cloud_img_json:
        json.dump(link_map, cloud_img_json)


def upload_to_bucket(file_stream, filename):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    client = storage.Client(project=cfg.PROJECT_ID)
    bucket = client.bucket(cfg.CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream.read(),
        content_type=mimetypes.guess_type(filename)[0])

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url


if __name__ == "__main__":
    upload_to_gcloud()
