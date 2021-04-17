from django.db import models
from django.http import request
from django.utils import timezone

class AccountInfoModel(models.Model):
    login_user_name = models.CharField(max_length=50, verbose_name="ユーザー名", default="", primary_key=True)
    login_user_email = models.EmailField(max_length=50, verbose_name="メールアドレス", default="")
    stripe_customer_id = models.CharField(max_length=50, verbose_name="会員ID",  default="") 
    stripe_register_date = models.DateTimeField(verbose_name="会員登録日", default=timezone.now)
    stripe_account_plan_title = models.CharField(max_length=50, verbose_name="契約プラン名", default="")
    stripe_account_plan = models.CharField(max_length=50, verbose_name="契約プランID", default="")
    stripe_subscription = models.CharField(max_length=50, verbose_name="サブスクリプションID", default="")
    stripe_account_status = models.BooleanField(verbose_name="課金状態", default=False)
    developer_flg = models.BooleanField(verbose_name="開発者フラグ", default=False)
    def __str__(self):
        return str(self.login_user_name)