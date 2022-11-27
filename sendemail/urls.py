from django.conf.urls import url

from .views import send_mail_view, success_view, image_load

urlpatterns = [
    url(r'^$', send_mail_view, name='send_mail'),
    url(r'success/$', success_view, name='success'),
    url(r'^image_load/$', image_load, name='image_load'),
]
