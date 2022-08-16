#!/usr/bin/env python3

import os
import requests

INPUT_PATH = '/data/feedback'
TXT_EXTENSION = '.txt'
URL = 'http://34.123.82.226/feedback/'

def get_feedback_files(dir_path):

    list_dir =  os.listdir(INPUT_PATH)
    for file in list_dir:
        file_path = os.path.join(INPUT_PATH, file)
        if os.path.isfile(file_path):
            file_name, file_extension = os.path.splitext(file)
            if file_extension == TXT_EXTENSION:
                print('Parsing information from file: {}'.format(file))
                feedback = get_feedback_from_file(file_path)
                upload_feedback(feedback)

def get_feedback_from_file(file_path):
    feedback = {}
    fields_read = 0
    with open(file_path, 'r') as feedback_file:
        while fields_read < 4:
            field_content = feedback_file.readline().strip()
            if fields_read == 0:
                feedback['title'] = field_content
            elif fields_read == 1:
                feedback['name'] = field_content
            elif fields_read == 2:
                feedback['date'] = field_content
            else:
                feedback['feedback'] = field_content
            fields_read += 1

    return feedback

def upload_feedback(feedback):
    response = requests.post(URL, json=feedback)
    if response.ok: 
       print('Success!, code {}'.format(response.status_code))
    else:
        print('Feedback not uploaded, the server replied with code {}'.format(response.status_code))

if __name__ == '__main__':
    get_feedback_files(INPUT_PATH)
