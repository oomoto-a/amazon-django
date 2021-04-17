from django.shortcuts import render
from django.views import generic

from asin.forms import ExclusionAsinsForm
from asin.models.exclusion_asins import ExclusionAsins


# 除外ASIN設定画面
class ExcludeASINView(generic.TemplateView):
    template_name = "asin/exclude_asin.html"
    form_class = "ExclusionAsinsForm"

    def get(self, request, *args, **kwargs):
        # 検索
        exclusion_asins = ExclusionAsins.objects.filter(account_id=self.request.user)

        if int(exclusion_asins.count()) >= 1:  
            asin_list = ""
            for asin in exclusion_asins:
                asin_list+=asin.asin + "\n"

            # 末尾改行削除
            asin_list = asin_list.rstrip('\n')
            data = dict(asins = asin_list)
            # formにセット
            form = ExclusionAsinsForm(initial=data)

            return render(request, self.template_name, {'form': form})

        # 対象ユーザに除外ASINが無い場合は新規登録
        form = ExclusionAsinsForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = ExclusionAsinsForm(request.POST)
        if form.is_valid():
            # チェックでエラーがない場合データを更新
            exclusion_asins = ExclusionAsins.objects.filter(account_id=self.request.user)
            exclusion_asins.delete()

            asins = request.POST['asins']
            if len(asins) != 0:
                asins = request.POST['asins'].split('\n')
                asins = list(filter(lambda a: a != '', asins))
                for asin_value in asins:
                    k = ExclusionAsins(account_id=request.user, 
                            asin=asin_value)
                    k.save()
                    ExclusionAsins.objects.all()

            params["result"] = "{}件".format(len(asins))

        params['form'] = form


        return render(request, self.template_name, params)

