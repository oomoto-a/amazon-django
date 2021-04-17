from django.shortcuts import render
from django.views import generic
from asin.const import Const
from asin.forms import AsinsForm, AsinsDisableForm
from asin.models.asin_setting import ASINSetting
from asin.models.asin_group_id import AsinGroupId
from asin.models.plan_master import PlanMaster
from asin.models.asin_collection_history import AsinCollectionHistory
from asin.common import calc_date
from my_page.models.account_info import AccountInfoModel
from datetime import datetime
from django.db.models import Sum

# ASIN設定画面
class ASINSettingView(generic.TemplateView):
    template_name = "asin/add_asin.html"
    form_class = "AsinsForm"

    def get(self, request, *args, **kwargs):
        args_asin_group_id = None
        if "asin_group_id" in kwargs:
            args_asin_group_id = kwargs["asin_group_id"]
        if args_asin_group_id is not None:
            # getリクエストでasin_group_idが指定された場合は検索
            asin_group_id_obj=AsinGroupId.objects.filter(account_id=self.request.user,
                                            asin_group_id=args_asin_group_id)
            # 該当するASIN設定一覧を取得
            if int(asin_group_id_obj.count())==1:  
                asin_setting_obj=ASINSetting.objects.filter(account_id=self.request.user,asin_group_id=asin_group_id_obj[0].asin_group_id)
                asins_str = ""
                asin_group_id = ""
                for asin in asin_setting_obj:
                    asins_str+=asin.asin + "\n"
                    asin_group_id=asin.asin_group_id
                # 末尾改行削除
                asins_str = asins_str.rstrip('\n')
                # formにセット
                data  = dict(asin_group_id=asin_group_id, asins=asins_str)
                if asin_group_id_obj[0].status == Const.KEEPA_API_STATUS_INIT:
                    # 未処理は編集可
                    form = AsinsForm(initial=data)
                else:
                    # 未処理以外は編集不可
                    form = AsinsDisableForm(initial=data)

                return render(request, self.template_name, {'form': form})

        # getリクエストでasin_group_idが指定ない場合は新規登録
        form = AsinsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = AsinsForm(request.POST)
        result = ""
        error_message = ""
        if form.is_valid():
            # チェックでエラーがない場合データを更新
            asin_group_id = request.POST.get("asin_group_id", None)
            group_id_obj=AsinGroupId.objects.filter(account_id=request.user,asin_group_id=asin_group_id)
            if group_id_obj.count() > 0 and group_id_obj[0].status != Const.KEEPA_API_STATUS_INIT:
                #KEEPAで未処理以外は登録不可
                error_message = "ASINグループID:{}は処理中または処理済みのため、別のASINグループ別のを入力して下さい".format(asin_group_id)
                params['form'] = form
                params['result'] = result
                params['error_message'] = error_message
                return render(request, self.template_name, params)

            # 累計処理数チェック
            mypage = AccountInfoModel.objects.filter(login_user_name=request.user).first()
            # 開発者はチェック無し
            if mypage.developer_flg :
                ASINSetting.update_data(request)
                result = request.POST['asin_group_id']
                params['form'] = form
                params['result'] = result
                return render(request, self.template_name, params)

            # 課金状態をみてNGなら終了
            paying_state_check = mypage.stripe_account_status
            if not paying_state_check:
                error_message = "課金がされていません。課金状態を確認して下さい。"
                params['form'] = form
                params['result'] = result
                params['error_message'] = error_message
                return render(request, self.template_name, params)

            dates = calc_date.calc_range(mypage.stripe_register_date, datetime.now(mypage.stripe_register_date.tzinfo))
            # 集計の範囲
            #  開始日
            start_date = dates[0]
            #  終了日
            end_date = dates[1]
            #プラン情報
            plan = PlanMaster.objects.filter(plan_id=mypage.stripe_account_plan).first()
            # プラン上限
            plan_limit = plan.month_limit
            query_account = "account_id = '{}' ".format(request.user)
            query_start =  "DATE(create_date) >= '{}' ".format(start_date)
            query_end   =  "DATE(create_date)  < '{}' ".format(end_date)
            sum = AsinCollectionHistory.objects.extra(where=[query_account, query_start, query_end]).aggregate(sum=Sum("asin_count"))
            sum_count = 0
            if sum is not None:
                sum_count = int(sum["sum"])

            asins = request.POST.get("asins", None)
            process_num = len(asins.split("\n"))

            if (sum_count + process_num) <= plan_limit:
                ASINSetting.update_data(request)
                result = request.POST['asin_group_id']
            else:
                error_message = "月上限処理数({})を超えています。処理済数：{},登録数：{}".format(plan_limit, sum_count, process_num)

        params['form'] = form
        params['result'] = result
        params['error_message'] = error_message
        return render(request, self.template_name, params)


