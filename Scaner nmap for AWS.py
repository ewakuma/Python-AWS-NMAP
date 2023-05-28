#!/usr/bin/env python

import nmap
import difflib
import smtplib
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

# AWS SES configuration
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
aws_region = 'YOUR_AWS_REGION'
ses_sender_email = 'SENDER_EMAIL@example.com'
ses_recipient_email = 'RECIPIENT_EMAIL@example.com'

# Scan configuration
server_addresses = ['IP_ADDRESS_1', 'IP_ADDRESS_2']  # List of IP addresses to scan
nmap_args = '-O -oN nmap_report.txt'  # Nmap scan arguments

# SMTP server configuration
smtp_server = 'YOUR_SMTP_SERVER'
smtp_port = YOUR_SMTP_PORT
smtp_sender_email = 'SENDER_EMAIL@example.com'
smtp_sender_password = 'SENDER_EMAIL_PASSWORD'
smtp_recipient_email = 'RECIPIENT_EMAIL@example.com'
smtp_recipient_name = 'Recipient Name'

while True:
    try:
        for server_address in server_addresses:
            # Perform Nmap scan
            nm = nmap.PortScanner()
            nm.scan(hosts=server_address, arguments=nmap_args)

            # Get previous scan results from file
            if os.path.exists('nmap_result.txt'):
                with open('nmap_result.txt', 'r') as f:
                    old_result = f.read().splitlines()
            else:
                old_result = []

            # Get new scan results and save them to file
            with open('nmap_report.txt', 'r') as f:
                new_result = f.read().splitlines()

            with open('nmap_result.txt', 'w') as f:
                f.write('\n'.join(new_result))

            # Find critical changes
            critical_changes = set(new_result).difference(set(old_result))

            # Check if there are critical changes
            if critical_changes:
                message = f'Warning, {smtp_recipient_name}!\n\n'
                message += 'Critical changes:\n\n'
                message += '\n'.join(critical_changes)
                message += '\n\nOld result:\n\n'
                message += '\n'.join(old_result)
                message += '\n\nNew result:\n\n'
                message += '\n'.join(new_result)

                # Send email using AWS SES
                ses_client = boto3.client(
                    'ses',
                    region_name=aws_region,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key
                )

                response = ses_client.send_raw_email(
                    Source=ses_sender_email,
                    Destinations=[ses_recipient_email],
                    RawMessage={
                        'Data': message
                    }
                )
                print('Email sent successfully via AWS SES.')

            else:
                print("Scan results have not changed")

        # Delay before the next scan
        time.sleep(60)

    except Exception as e:
        print(f"An error occurred: {e}")
