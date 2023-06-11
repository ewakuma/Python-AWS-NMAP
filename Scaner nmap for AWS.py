#!/usr/bin/env python

import nmap
import difflib
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
            message = f'Увага!\n\n'
            message += 'Критичні зміни:\n\n'
            message += '\n'.join(critical_changes)
            message += '\n\nПопередні результати:\n\n'
            message += '\n'.join(old_result)
            message += '\n\nНові результати:\n\n'
            message += '\n'.join(new_result)

            # Відправка електронної пошти за допомогою smtplib
            HOST = "localhost"
            SUBJECT = "Критичні зміни в результаті сканування"
            TO = "vasyl.haliuk@h-x.technology"
            FROM = "vasyl.haliuk@h-x.technology"
            text = message

            BODY = "\r\n".join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "Subject: %s" % SUBJECT,
                "",
                text.encode('utf-8')
            ))

            server = smtplib.SMTP(HOST)
            server.sendmail(FROM, [TO], BODY)
            server.quit()

            print('Електронний лист успішно відправлений через smtplib.')
        else:
            print("Результати сканування не змінилися")

except Exception as e:
    print(f"Сталася помилка: {e}")
