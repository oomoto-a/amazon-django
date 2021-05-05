from django.db import models
from datetime import datetime


# 人口テーブル
class Population(models.Model):
    prefectures_code = models.CharField(max_length=10,verbose_name="都道府県コード", null=False) 
    prefectures = models.CharField(max_length=10,verbose_name="都道府県", null=False) 
    era =  models.CharField(max_length=500, verbose_name="元号", null=False)
    jp_calendar =  models.CharField(max_length=500, verbose_name="和暦", null=False)
    year =  models.CharField(max_length=500, verbose_name="西暦", null=False)
    population =  models.CharField(max_length=500, verbose_name="人口", null=False)
    man =  models.CharField(max_length=500, verbose_name="男", null=False)
    woman =  models.CharField(max_length=500, verbose_name="女", null=False)
    create_date = models.DateTimeField(default=datetime.now, null=True, verbose_name="登録日")

    def __str__(self):
        return self.prefectures
