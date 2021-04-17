from django.db import models
from datetime import datetime


# ASINグループIDテーブル 
class AsinGroupId(models.Model):
    account_id = models.CharField(max_length=30,verbose_name="アカウントID", null=False) 
    asin_group_id = models.CharField(max_length=100, verbose_name="ASINグループID", null=False)
    asin_count =  models.IntegerField(verbose_name="登録ASIN数",default=0)
    status =  models.CharField(max_length=10, verbose_name="ステータス")
    create_date = models.DateTimeField(default=datetime.now, verbose_name="登録日")
    complete_date = models.DateTimeField(verbose_name="データ取得完了日", null=True)
    crawl_date = models.DateTimeField(verbose_name="クロール日時", null=True)

    def __str__(self):
        return self.account_id
