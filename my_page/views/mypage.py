from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

# ここから追加ライブラリ
from my_page.models.account_info import AccountInfoModel
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class MypageView(generic.TemplateView):
    model = AccountInfoModel
    template_name = "my_page/mypage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ログインしているユーザー名とメールアドレスを取得
        user_name = self.request.user
        user_email = self.request.user.email

        # ログインユーザー名をキーにして、ログインユーザーのストライプIDを取得する
        try:
            user_model = AccountInfoModel.objects.get(pk=user_name)
            account_plan = user_model.stripe_account_plan_title
            account_status = user_model.stripe_account_status

            if account_plan == "":
                account_plan = "プラン選択なし"
                account_status = "未契約"
            else:
                if account_status == True:
                    account_status = "支払い済"
                
        except:
            account_plan = "プラン選択なし"
            account_status = "未契約"

        # contextに追加(htmlで使える)
        context['account_plan'] = account_plan
        context['account_status'] = account_status

        return context