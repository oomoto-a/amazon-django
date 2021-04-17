from django.db import models
from django.http import request
from bulk_update.helper import bulk_update
import datetime

from .asin_group_id import ASINGroupIdModel

# ASIN設定モデル
class ASINSettingModel (models.Model):
    account_id = models.CharField(
        max_length=30, default="", verbose_name="アカウントID")  # 非表示
    asin_group_id = models.CharField(
        max_length=50, default="", verbose_name="取得ID")
    asin = models.CharField(max_length=10, default="", verbose_name="ASIN")

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
        asin = request.POST.get("asin", None)
        asin_group_id = request.POST.get("asin_group_id", None)
        reserve_date = now  # 現在日時をセット
        asin_list = asin.split("\n")

        # asin_group_idの重複確認し、なければ追加
        asin_group_id_obj=ASINGroupIdModel.objects.filter(account_id=request.user,asin_group_id=asin_group_id)
        if asin_group_id_obj.count()==0:
            # 取得IDを追加
            update_data = ASINGroupIdModel(
                asin_group_id=asin_group_id, reserve_date=reserve_date, account_id=request.user)
            update_data.save()

        # 更新の場合
        else:
            # ASINリストを一旦削除
            ASINSettingModel.objects.filter(asin_group_id=asin_group_id,account_id=request.user).delete()
        
        # ASINリストを追加
        setting_list=[]
        for asin in asin_list:
            if len(asin) >= 2:  # 空白行は除去するために２文字以上に限定する
                setting_list.append(ASINSettingModel(asin=asin, asin_group_id=asin_group_id,
                                                        account_id=request.user))
        # 一括データ作成
        ASINSettingModel.objects.bulk_create(setting_list)

