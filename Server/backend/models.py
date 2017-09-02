# https://github.com/google/google-api-python-client/blob/master/samples/django_sample/plus/models.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.contrib.django_util.storage import DjangoORMStorage

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class CredentialsAdmin(admin.ModelAdmin):
    pass
