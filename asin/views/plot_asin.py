from django.shortcuts import render
from django.views import generic
from asin.models.keepa_info import KeepaInfo
from asin.forms import PlotForm
# グラフ画面
class PlotAsin(generic.TemplateView):
    template_name = "asin/plot_asin.html"
    form_class = "PlotForm"
    def get(self, request, id, *args, **kwargs):
        keepaInfo = KeepaInfo.objects.filter(
            id = id, 
            account_id = request.user,)

        
        fbm = request.GET.get("fbm")
        fba = request.GET.get("fba")
        cart = request.GET.get("cart")

        form = None
        if fbm is None and fba is None and cart is None:
            form = PlotForm({"fbm":True,"fba":True,"cart":True,})
        else:
            form = PlotForm(request.GET)
        required = ""
        if not keepaInfo[0].lowest_history_fbm and not keepaInfo[0].lowest_history_fba and not keepaInfo[0].buy_box_history:
            required = "対象のデータがありません"
        params={
            "id":id,
            "account_id":request.user,
            "title": keepaInfo[0].title,
            "required": required,
            "form": form
        }
        return render(request, self.template_name, params)
