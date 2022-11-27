# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from PIL import Image

import json

from .forms import SendEmail
from .tasks import send_message_task


def send_mail_view(request):
    if request.method == 'GET':
        form = SendEmail()
    elif request.method == 'POST':
        form = SendEmail(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            send_to = json.load(request.FILES['send_to'])
            from_email = form.cleaned_data['from_email']
            template_text = request.FILES['template'].read()
            delay = form.cleaned_data['delay']
            image_url = request.build_absolute_uri(reverse('image_load'))
            try:
                send_message_task.apply_async(
                    (subject, template_text, from_email, send_to, image_url),
                    delay=delay
                )
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма')
            return redirect('success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, 'email.html', {'form': form})


def success_view(request):
    return HttpResponse('Сообщение отправлено')


def image_load(request):
    print("\nEmail opened\n")
    image = Image.new('RGB', (1, 1))
    response = HttpResponse(content_type="image/png")
    image.save(response, 'PNG')
    return response
