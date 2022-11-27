# -*- coding: utf-8 -*-
from django import forms


class SendEmail(forms.Form):
    subject = forms.CharField(label='Тема', required=True)
    from_email = forms.EmailField(label='Отправитель', required=True)
    send_to = forms.FileField(label='Получатель', required=True)
    template = forms.FileField(label='Шаблон', required=True)
    delay = forms.IntegerField(label='Отложить отправку (время в минутах)')
