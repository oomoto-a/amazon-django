from django.db import models
from django.http import request

# ASINグループIDモデル
class ASINGroupIdModel (models.Model):
    account_id = models.CharField(
        max_length=30, default="", verbose_name="アカウントID")  # 非表示
    asin_group_id = models.CharField(
        max_length=50, default="", verbose_name="ASINグループID")
    reserve_date = models.DateTimeField(null=True, verbose_name="予約日")
    end_date = models.DateTimeField(null=True, verbose_name="取得完了日")