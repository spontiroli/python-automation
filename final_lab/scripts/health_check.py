#!/usr/bin/env python3

import os
import sys
import socket
import psutil
import emails
from socket import error as socket_error

def check_cpu_usage(max_percentage):
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage > max_percentage

def check_available_disk(min_percentage):
    disk_usage = psutil.disk_usage('/')
    total = disk_usage.total
    free = disk_usage.free
    percentage = (free * 100) / total
    return percentage < min_percentage

def check_available_memory(min_memory):
    memory = psutil.virtual_memory()
    available = round(memory.available / (1024**2))
    return available < min_memory

def check_name_resolution(host_name, host_address):
    # socket.gethostbyname is deprecated, prefer socket.getaddrinfo
    # https://stackoverflow.com/questions/2805231/how-can-i-do-dns-lookups-in-python-including-referring-to-etc-hosts
    address = list(
        i        # raw socket structure
            [4]  # internet protocol info
            [0]  # address
        for i in 
        socket.getaddrinfo(
            host_name,
            0  # port, required
        )
        if i[0] is socket.AddressFamily.AF_INET  # ipv4

        # ignore duplicate addresses with other socket types
        and i[1] is socket.SocketKind.SOCK_RAW
    )

    return address[0] == host_address

def notify_issue(issue):
    sender = 'automation@example.com'
    # when using CRON we have to change the following line since os.environ['USER'] will fail if we don't set up the variables properly
    receiver = '{}@example.com'.format(os.environ['USER'])
    body = 'Please check your system and resolve the issue as soon as possible.'
    message = emails.generate_email(sender, receiver, issue, body)
    emails.send_email(message)

if __name__ == '__main__':

    # -Report if CPU usage is over 80%. Subject: 'Error - CPU usage is over 80%'
    # -Report if available disk space if lower than 20%. Subject: 'Error - Available disk space is less than 20%'
    # -Report if available memory is less than 500MB. Subject: 'Error - Available memory is less than 500MB'
    # -Report if 'localhost'cannot be resolved to '127.0.0.1'. Subject: 'Error - localhost cannot be resolved to 127.0.0.1'
    # -Add script to crontab and run it every 60 seconds
    # -If some issue is detected send an email from 'automation@example.com' to 'username@example.com' (username is $USER)
    # with the proper subject and body: 'Please check your system and resolve the issue as soon as possible.' (no attachment)

    try:

        if check_cpu_usage(80):
            issue = 'Error - CPU usage is over 80%'
            notify_issue(issue)

        if check_available_disk(20):
            issue = 'Error - Available disk space is less than 20%'
            notify_issue(issue)

        if check_available_memory(500):
            issue = 'Error - Available memory is less than 500MB'
            notify_issue(issue)

        if check_name_resolution('localhost', '127.0.0.1'):
            issue = 'Error - localhost cannot be resolved to 127.0.0.1'
            notify_issue(issue)

    except ConnectionError as cerror:

        print('Failed  to send email, verify network settings and server configuration. Description: {}.'.format(cerror))

