#!/usr/bin/env python

import nmap
import difflib
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

# Конфігурація AWS SES
aws_access_key_id = 'ВАШ_КЛЮЧ_ДОСТУПУ_AWS'
aws_secret_access_key = 'ВАШ_СЕКРЕТНИЙ_КЛЮЧ_ДОСТУПУ_AWS'
aws_region = 'ВАША_ОБЛАСТЬ_AWS'
ses_sender_email = 'ВІДПРАВНИК_ЕЛЕКТРОННОЇ_ПОШТИ@example.com'
ses_recipient_email = 'ОТРИМУВАЧ_ЕЛЕКТРОННОЇ_ПОШТИ@example.com'

# Конфігурація сканування
server_addresses = ['IP_АДРЕСА_1', 'IP_АДРЕСА_2']  # Список IP-адрес для сканування
nmap_args = '-O -oN nmap_report.txt'  # Аргументи сканування Nmap

try:
    for server_address in server_addresses:
        # Виконуємо сканування Nmap
        nm = nmap.PortScanner()
        nm.scan(hosts=server_address, arguments=nmap_args)

        # Отримуємо попередні результати сканування з файлу
        if os.path.exists('nmap_result.txt'):
            with open('nmap_result.txt', 'r') as f:
                old_result = f.read().splitlines()
        else:
            old_result = []

        # Отримуємо нові результати сканування та зберігаємо їх в файл
        with open('nmap_report.txt', 'r') as f:
            new_result = f.read().splitlines()

        with open('nmap_result.txt', 'w') as f:
            f.write('\n'.join(new_result))

        # Знаходимо критичні зміни
        critical_changes = set(new_result).difference(set(old_result))

        # Перевіряємо, чи є критичні зміни
        if critical_changes:
            message = f'Увага, {smtp_recipient_name}!\n\n'
            message += 'Критичні зміни:\n\n'
            message += '\n'.join(critical_changes)
            message += '\n\nПопередні результати:\n\n'
            message += '\n'.join(old_result)
            message += '\n\nНові результати:\n\n'
            message += '\n'.join(new_result)

            # Надсилаємо електронну пошту за допомогою AWS SES
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
            print('Електронна пошта успішно відправлена через AWS SES.')

        else:
            print("Результати сканування не змінилися")

except Exception as e:
    print(f"Сталася помилка: {e}")
