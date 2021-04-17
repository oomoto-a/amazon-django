from django.db import models
from datetime import datetime

# 除外ワードテーブル
class ExclusionWord(models.Model):
    account_id = models.CharField("アカウントID",max_length=30, null=False) 
    word =  models.CharField(max_length=100, verbose_name="除外ワード", null=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name="登録日")

    def __str__(self):
        return self.account_id
