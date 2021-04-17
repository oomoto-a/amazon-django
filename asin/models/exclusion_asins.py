from django.db import models
from datetime import datetime

# 除外ASINテーブル
class ExclusionAsins(models.Model):
    account_id = models.CharField("アカウントID",max_length=30, null=False) 
    asin =  models.CharField(max_length=10, verbose_name="除外ASIN", null=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name="登録日")

    def __str__(self):
        return self.account_id
