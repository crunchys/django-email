# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_message_task(subject, template_text, from_email, subscribers_list, image_url):
    with open('template_file.html', 'w') as f:
        f.write(template_text)
    i = 0
    for _ in range(len(subscribers_list['subscribers'])):
        html_message = render_to_string('template_file.html',
                                        {
                                            'name': subscribers_list['subscribers'][i]['name'],
                                            'birthday': subscribers_list['subscribers'][i]['birthday'],
                                            'image_url': image_url
                                        })
        send_to = (subscribers_list['subscribers'][i]['email'],)
        send_mail(
            '%s от %s' % (subject, from_email),
            html_message,
            from_email,
            send_to,
            html_message=html_message
        )
        i += 1

    os.remove('template_file.html')
