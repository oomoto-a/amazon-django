from django.db import models
from datetime import datetime


# asin収集履歴テーブル
class AsinCollectionHistory(models.Model):
    account_id = models.CharField(max_length=30,verbose_name="アカウントID", null=False) 
    asin_group_id = models.CharField(max_length=100, verbose_name="asinグループID", null=False)
    asin_count =  models.CharField(max_length=500, verbose_name="取得成功したASIN数", null=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name="登録日")

    def __str__(self):
        return self.account_id
