#!/usr/bin/env python3
import re
import os
import operator
import sys
import csv

# I/O
LOG_FILE = 'syslog.log'
ERROR_STATISTICS = 'error_message.csv'
USER_STATISTICS = 'user_statistics.csv'

# Statistics
per_user = {}
error = {}

# Functions
def parse_log(log_file):
    with open(log_file, 'r') as log:
        for line in log:
            # let's read the log file line by line
            # the strip() method removes any leading (spaces at the beginning) and trailing (spaces at the end)
            entry = line.strip()
            entry = re.search(r"(?P<message_type>ERROR|INFO) (?P<message>[\w ]*).*\((?P<username>\w*\.?\w*)\)", line)
            type = entry.group('message_type')
            message = entry.group('message').strip()
            username = entry.group('username')

            if type == 'ERROR':
                if not message in error:
                    error[message] = 1
                else:
                    error[message] += 1

                if not username in per_user:
                    per_user[username] = {}
                    per_user[username]['error'] = 1
                    per_user[username]['info'] = 0
                else:
                    per_user[username]['error'] += 1

            elif type == 'INFO':
                if not username in per_user:
                    per_user[username] = {}
                    per_user[username]['error'] = 0
                    per_user[username]['info'] = 1
                else:
                    per_user[username]['info'] +=1
            else:
                print("Nothing to do here...")

def export_error_messages(error_statistics, csv_error_file):
    print(f'Saving {error_statistics} into {csv_error_file}')
    error_statistics = sorted(error_statistics.items(), key=operator.itemgetter(1), reverse = True)
    print(f'Sorted error list is: {error_statistics}')

    with open(csv_error_file, 'w') as csv_output:
        fields = ['Error', 'Count']
        csv_writer = csv.DictWriter(csv_output, fieldnames=fields)
        csv_writer.writeheader()
        for e in error_statistics:
            csv_writer.writerow({'Error': e[0], 'Count': e[1]})
            print(e)

def export_user_messages(user_statistics, csv_user_file):
    print(f'Saving {user_statistics} into {csv_user_file}')
    user_statistics = sorted(user_statistics.items(), key=operator.itemgetter(0))
    print(f'Sorter user list is: {user_statistics}')

    with open(csv_user_file, 'w') as csv_output:
        fields = ['Username', 'INFO', 'ERROR']
        csv_writer = csv.DictWriter(csv_output, fieldnames = fields)
        csv_writer.writeheader()
        for m in user_statistics:
            #info_stat = stats['info']
            #error_stat = stats['error']
            print(m)
            csv_writer.writerow({'Username': m[0], 'INFO': m[1]['error'], 'ERROR': m[1]['info']})


if __name__ == '__main__':
    parse_log(LOG_FILE)
    export_error_messages(error, ERROR_STATISTICS)
    export_user_messages(per_user, USER_STATISTICS)
