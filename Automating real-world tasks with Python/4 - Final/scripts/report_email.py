#!/usr/bin/env python3

# TODO
# -Send email
# From: automation@example.com
# To: username@example.com (username is the current $USER)
# Subject: Upload Completed - Online Fruit Store
# Body: All fruits are uploaded to our website successfully. A detailed list is attached to this email.
# Attachment: /tmp/processed.pdf

# TODO
# -Generate a PDF report (save it to /tmp/processed.pdf) using ReportLab library, the report should look like this:
# Processed Update on [TODAYS_DATE]
# [blank line]
# name: Apple
# weight: 500 lbs
# [blank line]
# name: Avocado
# weight: 200 lbs

import os
import datetime
import reports
import emails
import sys
import errno
from socket import error as socket_error

def process_data(path):
    # returns all fruit information, then used as the 'info' parameter for the reports.generate_report() function
    files = os.listdir(path)
    fruits = ''
    for file in files:

        full_path = ''.join([path, file])
        print(full_path)
        if os.path.isfile(full_path):
            if file.endswith('.txt'):
                # it's a TXT file
                with open(full_path, 'r') as fruit:

                    fields = fruit.readlines()
                    name = fields[0]
                    weight = fields[1]
                    fruits += ''.join(['name: ' + name, 'weight: ' + weight])
                    fruits += '\n' 
    return fruits


if __name__ == '__main__':

    # generate the PDF report
    report_path = '/tmp/processed.pdf'
    current_date = datetime.datetime.now().strftime('%B %d, %Y')
    title = ''.join(['Processed Update on ', current_date])
    
    home = os.path.expanduser('~')
    supplier_descriptions = 'supplier-data/descriptions/'
    full_path = os.path.join(home, supplier_descriptions)

    all_fruits = process_data(full_path)
    all_fruits = all_fruits.replace('\n','<br/>')
    reports.generate_report(report_path, title, all_fruits)

    try:
        # send the PDF report by email
        sender = 'automation@example.com'
        receiver = '{}@example.com'.format(os.environ.get('USER'))
        subject = 'Upload Completed - Online Fruit Store'
        body = 'All fruits are uploaded to our website successfully. A detailed list is attached to this email.'
        message = emails.generate_email(sender, receiver, subject, body, report_path)
        emails.send_email(message)
    except socket_error as serr:
        print('Failed to send email. Description: {}'.format(serr))
        sys.exit(1)
