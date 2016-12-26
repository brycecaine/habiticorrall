from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>\w+)/?$', views.profile, name='profile'),
    url(r'^tasks/(?P<username>\w+)/?$', views.tasks, name='tasks'),
    url(r'^score/(?P<username>[\w\-]+)/(?P<task_id>[\w\-]+)/?$', views.score, name='score'),
]