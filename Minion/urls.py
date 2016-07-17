from django.conf.urls import url

from . import views

urlpatterns = [
    url('train/(?P<session_id>.*)', views.train, name='train'),
    url('run/(?P<session_id>.*)', views.run, name='run'),
]