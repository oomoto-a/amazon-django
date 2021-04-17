from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib import messages

from data_view.forms.asin_setting import *
from data_view.models.asin_setting import *
from data_view.models.asin_group_id import *


# ASIN設定画面
class ASINSettingView(generic.TemplateView):
    template_name = "data_view/asin-setting.html"
    form_class = "ASINSettingForm"

    def get(self, request, *args, **kwargs):
        # getリクエストでasin_group_idが指定された場合は検索
        if request.GET.get("asin_group_id"):
            asin_group_id_obj=ASINGroupIdModel.objects.filter(account_id=self.request.user,asin_group_id=request.GET.get("asin_group_id"))
            # 該当するASIN設定一覧を取得
            if int(asin_group_id_obj.count())==1:  
                asin_setting_obj=ASINSettingModel.objects.filter(account_id=self.request.user,asin_group_id=asin_group_id_obj[0].asin_group_id)
                asin_setting_form=""
                for asin in asin_setting_obj:
                    asin_setting_form+=asin.asin + "\n"
                # formにセット
                data=ASINSettingModel()
                data.asin_group_id=asin_group_id_obj[0].asin_group_id
                data.asin=asin_setting_form
                form = ASINSettingForm(instance=data)
                return render(request, self.template_name, {'form': form})
        #data = ASINSettingModel.get_data(ASINSettingModel, request)
        # if data != None:
        #    form = ASINSettingForm(instance=data)
        # else:
        #    form = ASINSettingForm()
        form = ASINSettingForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        AJAXで呼ばれるので、returnは返さない
        '''
        # データを更新
        ASINSettingModel.update_data(request)

        # 画面に反映
        #data = ASINSettingModel.get_data(ASINSettingModel, request)
        # if data != None:
        #    form = ASINSettingForm(instance=data)
        # else:
        #    form = ASINSettingForm()
        form = ASINSettingForm()

        return render(request, self.template_name, {'form': form})


