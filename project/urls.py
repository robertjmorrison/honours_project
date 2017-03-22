from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # example: /home/
    url(r'^$', views.index, name='index'),
    # example: /home/session/3
    url(r'^session/(?P<game_id>[0-9]+)/$', views.session, name='session'),
    # example: /home/session/3/2
    url(r'^session/(?P<game_id>[0-9]+)/(?P<play_id>[0-9]+)/$', views.session, name='session')
]
