from django.db import models
from datetime import datetime


# プランマスター
class PlanMaster(models.Model):
    plan_id = models.CharField(max_length=30,verbose_name="プランID", null=False) 
    plan_name = models.CharField(max_length=100, verbose_name="プラン名", null=False)
    month_limit =  models.IntegerField(verbose_name="月使用上限数", null=False)
    create_date = models.DateTimeField(default=datetime.now, verbose_name="登録日")

    def __str__(self):
        return self.plan_name
