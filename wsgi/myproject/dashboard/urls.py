from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score/(?P<user_id>[\w\-]+)/(?P<task_id>[\w\-]+)/?$', views.score, name='score'),
]