from django.conf.urls import url

from . import views

urlpatterns = [
    url('trainingsessions', views.trainingsessions, name='trainingsessions'),
    url('runningsessions', views.runningsessions, name='runningsessions'),
    url('statusurl/(?P<session_id>.*)', views.statusurl, name='statusurl'),
    url('state/(?P<session_id>.*)', views.state, name='state'),
    url('delete/(?P<session_id>.*)', views.delete, name='delete'),
    url('train/(?P<session_id>.*)', views.train, name='train'),
    url('run/(?P<session_id>.*)', views.run, name='run'),
    url('health', views.health, name='health'),
]