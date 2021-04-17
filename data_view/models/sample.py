from django.db import models
from django.http import request

# Sampleモデル
class SampleModel(models.Model):
    account_id = models.CharField("アカウントID",max_length=30, null=False) 
