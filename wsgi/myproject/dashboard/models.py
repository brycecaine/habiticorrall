from __future__ import unicode_literals

from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    user_id = models.CharField(max_length=200)
    api_token = models.CharField(max_length=200)
