from django.conf.urls import url

from . import views

urlpatterns = [
    url('index/(?P<temp_id>\w*)', views.index, name='index'),
]