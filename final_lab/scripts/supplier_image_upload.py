#!/usr/bin/env python3

# TODO
# -Take JPEG images from ~/supplier-data/images and upload them to http://localhost/upload/

import requests
from requests.exceptions import ConnectionError
import os
import sys

if __name__ == '__main__':

    url = "http://localhost/upload/"
    home = os.path.expanduser('~')
    images_folder = 'supplier-data/images/'
    full_path = os.path.join(home, images_folder)

    images = os.listdir(full_path)
    
    for image in images:
        if image.endswith(".jpeg"):
            image_path = os.path.join(full_path, image)
            print('Uploading {}'.format(image_path))
            
            with open(os.path.join(image_path), 'rb') as opened:
                try:
                    response = requests.post(url, files={'file': opened})
                    if response.ok:
                        print('Success!')
                    else:
                        print('Failed to upload. Error Code is {}'.format(response.status_code))
                except ConnectionError:
                    print('Upload failed, verify network settings and API endpoint.')
                    print('Aborting upload.')
                    sys.exit(1)
