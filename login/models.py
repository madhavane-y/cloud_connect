from django.db import models
from django import forms

# Create your models here.

class account(models.Model):

    # IAM id
    iam = models.CharField("Region of IAM",max_length=15)
    # Alias
    alias = models.CharField("API Key",max_length=50)
    # password
    passwd = models.CharField("Secret Key",max_length=80)

    # def listable(self):
    #     return self.objects.all()

    def __str__(self):
        return self.alias
