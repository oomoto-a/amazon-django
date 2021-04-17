from django.shortcuts import render
from django.views import generic

from asin.forms import ExclusionWordForm
from asin.models.exclusion_word import ExclusionWord


# ASIN設定画面　除外ワード画面
class ExcludeWordView(generic.TemplateView):
    template_name = "asin/exclude_word.html"
    form_class = "ExclusionWordForm"

    def get(self, request, *args, **kwargs):
        # 検索
        exclusion_word = ExclusionWord.objects.filter(account_id=self.request.user)

        if int(exclusion_word.count()) >= 1:  

            words = ""
            for exclusion_word in exclusion_word:
                words+=exclusion_word.word + "\n"

            # 末尾改行削除
            words = words.rstrip('\n')
            # formにセット
            data = dict(word=words)
 
            form = ExclusionWordForm(initial=data)

            return render(request, self.template_name, {'form': form})

        # 対象ユーザに除外wordが無い場合は新規登録
        form = ExclusionWordForm()
        return render(request,  self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        登録ボタン押下時
        '''
        params = {'result': '', 'form': None}
        form = ExclusionWordForm(request.POST)
        if form.is_valid():
            # チェックでエラーがない場合データを更新
            exclusion_word = ExclusionWord.objects.filter(account_id=self.request.user)
            exclusion_word.delete()

            words = request.POST['word']
            if len(words) != 0:
                words = words.split('\n')
                words = list(filter(lambda a: a != '', words))
                for word in words:
                    k = ExclusionWord(account_id=request.user, 
                            word=word)
                    k.save()
                    ExclusionWord.objects.all()

            params["result"] = "{}件".format(len(words))

        params['form'] = form

        return render(request, self.template_name, params)

