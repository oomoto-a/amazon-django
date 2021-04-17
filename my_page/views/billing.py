from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

# ここから追加ライブラリ
from django.conf import settings
import stripe
from my_page.models.account_info import AccountInfoModel
from asin.models.plan_master import PlanMaster
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from urllib.parse import urlencode


stripe.api_key = settings.STRIPE_SECRET_KEY

# class BillingView(generic.TemplateView):
class BillingView(generic.ListView):
    model = PlanMaster
    template_name = "my_page/billing.html"

    def post(self, request, *args, **kwargs):

        # ログインしているユーザー名とメールアドレスを取得
        user_name = self.request.user
        user_email = self.request.user.email
        # ログインユーザー名をキーにしてモデルを取得する
        try:
            user_model = AccountInfoModel.objects.get(pk=user_name)
        # マイページ用のモデルが無い時は作成する
        except:
            object = AccountInfoModel.objects.create(
                    login_user_name=user_name,
                    login_user_email=user_email,
                    )
            user_model = AccountInfoModel.objects.get(pk=user_name)

        """支払うボタンが押された時"""
        if request.POST["button"] == 'buy_button':

            token = request.POST['stripeToken']  # フォームでのサブミット後に自動で作られる

            # product_list = stripe.Product.list() stripeに存在する商品を全部取り出せるが使い道なさそう       
            plan = request.POST['plan'] # 選択プラン
            plan_id = plan[:plan.find(',')]
            plan_title = plan[plan.find(',')+1:]

            # DBにカスタマーIDが無い場合(stripeに登録されていない場合)
            if "cus" not in user_model.stripe_customer_id:

                # stripe側にカスタマー情報が存在していないか確認
                customer_list = stripe.Customer.list()

                for customer in customer_list["data"]:
                    # stripeにもし同じアドレスが存在していた場合、そのIDを用いる。
                    if customer["email"] == user_email:
                        user_model.stripe_customer_id = customer["id"]
                        user_model.save()
                        break
                else:
                    # stripeに同じアドレスが存在しない時、stripeに顧客情報の登録
                    customer = stripe.Customer.create(
                        name=user_name,
                        email=user_email,
                        source=token, #トークン、クレカ情報はここ
                        )
                    # カスタマーIDをDBに登録
                    user_model.stripe_customer_id = customer.id
                    user_model.save()
                    
            # サブスクリプションIDがDBに無い場合
            if "sub" not in user_model.stripe_subscription:
                # サブスクリプションの開始 (顧客とプランを紐付け)
                subscription = stripe.Subscription.create(
                    customer=user_model.stripe_customer_id,
                    items=[
                        {
                        "plan": plan_id, 
                        },
                    ]
                    )

                # 支払い開始日
                payment_startdatetime = datetime.now()

                # モデルに登録
                user_model.stripe_register_date = payment_startdatetime
                user_model.stripe_account_plan = plan_id
                user_model.stripe_account_plan_title = plan_title
                user_model.stripe_subscription = subscription.id
                user_model.stripe_account_status = True
                user_model.save()

                parameters = urlencode({'result': '登録に成功しました'})
        
            else:
                # パラメータのdictをurlencodeする。複数のパラメータを含めることも可能
                parameters = urlencode({'result': '既にプランに登録済です'})
            

        """クレカ情報の変更時"""
        if request.POST["button"] == 'modify_button':

            token = request.POST['stripeToken']  # フォームでのサブミット後に自動で作られる

            if "cus" not in user_model.stripe_customer_id:
                parameters = urlencode({'result': 'お客様IDが存在しません'})
            else:
                customer = stripe.Customer.modify(
                            user_model.stripe_customer_id,
                            source=token, #トークン
                            )
                parameters = urlencode({'result': 'クレジットカード情報を変更しました'})
                

        """解約時"""
        if request.POST["button"] == 'cancel_button':

            if "sub" not in user_model.stripe_subscription:
                parameters = urlencode({'result': 'お客様は契約しておりません'})
            else:
                try:
                    stripe.Subscription.delete(user_model.stripe_subscription)
                    parameters = urlencode({'result': '解約しました'})

                    user_model.stripe_subscription = ""
                    user_model.stripe_account_plan = ""
                    user_model.stripe_account_plan_title = ""
                    user_model.stripe_account_status = False
                    user_model.save()
                except:
                    parameters = urlencode({'result': 'お客様に登録されているサブスクリプションIDがStripeに存在しません。管理者にお問い合わせください。'})

        """リダイレクト"""
        # リダイレクト先のパスを取得する
        redirect_url = reverse('my_page:redirectpage')
        # URLにパラメータを付与する
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
    
    # as_view()の時点で呼び出される
    def get_context_data(self, **kwargs):
        """STRIPE_PUBLIC_KEYを渡したいだけ"""
        context = super().get_context_data(**kwargs)
        context['publick_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def redirect_view(request):
    result = request.GET.get('result')
    context = {'result': result} 

    return render(request, 'my_page/redirect.html', context)