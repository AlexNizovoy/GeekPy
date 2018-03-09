from api.celery import app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time

from django.template.loader import render_to_string

import api.config as cfg
from hn_parser.helpers import parse_stories, write_records


@app.task
def parsing(category_name, email, base_url=None):
    t0 = time.time()
    data = parse_stories(category_name)
    t1 = time.time()
    count = write_records(data)
    t2 = time.time()
    context = {'email': email,
               'category_name': category_name,
               'count': count,
               'time_parse': t1 - t0,
               'time_write': t2 - t1,
               'time_total': t2 - t0,
               'base_url': base_url
               }
    send_mail(**context)


def send_mail(**kwargs):
    addr_from = cfg.EMAIL_FROM
    addr_to = kwargs.get('email') or cfg.EMAIL_REPORT_FALLBACK
    passwd = cfg.EMAIL_PASSWORD

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Звіт про роботу парсера'
    msg['From'] = addr_from
    msg['To'] = addr_to
    html = render_to_string('api/email.html', context=kwargs, request=kwargs.get('request'))
    text = render_to_string('api/plain_text.html', context=kwargs)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(addr_from, passwd)
    server.sendmail(addr_from, addr_to, msg.as_string())
    server.quit()
