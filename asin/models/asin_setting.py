from django.db import models
from django.http import request
from bulk_update.helper import bulk_update
import datetime

from .asin_group_id import AsinGroupId
from asin.const import Const

# ASIN設定
class ASINSetting (models.Model):
    account_id = models.CharField(max_length=30, default="", verbose_name="アカウントID")  # 非表示
    asin_group_id = models.CharField(max_length=50, default="", verbose_name="asinグループID")
    asin = models.CharField(max_length=10, default="", verbose_name="ASIN")
    status =  models.CharField(max_length=10, verbose_name="ステータス")

    # データ取得
    def get_data(self, request):
        data_list = self.objects.filter(account_id=request.user)
        data = self.objects.filter(account_id=request.user).first()

        # データが存在する場合
        if len(data_list) >= 1:
            # 現状の設定値を反映
            asin = ""
            for d in data_list:
                asin += d.asin + "\n"
            data.asin = asin
            return data
        # データが存在しない場合
        else:
            return None

    # データ更新
    @ staticmethod
    def update_data(request):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asins = request.POST.get("asins", None)
        asin_group_id = request.POST.get("asin_group_id", None)
        asin_list = asins.split("\n")
        if "" in asin_list:
            asin_list.remove("")
        
        # asin_group_id
        group_id_obj=AsinGroupId.objects.filter(account_id=request.user,asin_group_id=asin_group_id)

        if group_id_obj.count() != 0:
            # ASINリストを一旦削除
            ASINSetting.objects.filter(asin_group_id=asin_group_id,account_id=request.user).delete()

        # 取得IDを数えなおしてインサートアップデート
        product, created = AsinGroupId.objects.update_or_create(
            asin_group_id=asin_group_id, account_id=request.user,
            defaults={"asin_count":len(asin_list),"status":Const.KEEPA_API_STATUS_INIT}
            )


        # ASINリストを追加
        setting_list=[]
        for asin in asin_list:
            if len(asin) >= 2:  # 空白行は除去するために２文字以上に限定する
                setting_list.append(ASINSetting(asin=asin, asin_group_id=asin_group_id,
                                                        account_id=request.user,status=Const.KEEPA_API_STATUS_INIT))
        # 一括データ作成
        ASINSetting.objects.bulk_create(setting_list)

