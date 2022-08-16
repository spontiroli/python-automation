#!/usr/bin/env python3

# TODO
# -Upload descriptions to http://localhost/fruits/
# -Descriptions are located at ~/supplier-data/descriptions
# -Descriptions have three fields: 'name', 'weight' (in lbs), and 'description' (drop the 'lbs' string and get the integer value)
# -Add 'image_name' key, that is the name of the TXT file with the description but with a '.jpeg' extension (i.e. 010.txt will have
# '010.jpeg' as the image name

import os
import requests
import sys
from requests.exceptions import ConnectionError

def process_fruits(path, url):

    fruits = {}
    files = os.listdir(path)

    for file in files:

        full_path = ''.join([path, file])
        file_name, file_extension = os.path.splitext(file)

        if os.path.isfile(full_path):
            if file.endswith('.txt'):
                # it's a TXT file
                with open(full_path, 'r') as fruit:
                    fields = fruit.readlines()
                    fruits['name'] = fields[0].strip('\n')
                    fruits['weight'] = fields[1].strip('\n').strip(' lbs')
                    fruits['description'] = fields[2].strip('\n').replace('\xa0','')
                    fruits['image_name'] = ''.join([file_name, '.jpeg'])
                    try:
                        response = requests.post(url, json=fruits)
                        if response.ok:
                            print('Success, uploaded {} to {}'.format(fruits['name'], url))
                        else:
                            print('Failed to upload {} to {}'.format(fruits['name'], url))
                        print('Server replied with Code {}'.format(response.status_code))
                    except ConnectionError:
                        print('Connection Error, please verify your network settings and the API endpoint.')
                        print('Aborting upload.')
                        sys.exit(1)

if __name__ == '__main__':

    fruits_api = 'http://localhost/fruits/'

    home = os.path.expanduser('~')
    supplier_descriptions = 'supplier-data/descriptions/'
    full_path = os.path.join(home, supplier_descriptions)

    process_fruits(full_path, fruits_api)
