from django.shortcuts import render
from django.views import generic
from django_tables2 import SingleTableView,MultiTableMixin
from django.views.generic.base import TemplateView
from django.views.generic import ListView, UpdateView, DeleteView
from asin.models.keepa_info import KeepaInfo
from . import table
from django.db import models
from asin.forms import SampleChoiceForm
from django_tables2 import RequestConfig 

class ResultView(MultiTableMixin, TemplateView):
    model = KeepaInfo
    table_class = table.KeepaInfoTable
    table_pagination = {"per_page": 1}
    per_page = 1
    template_name = "asin/disp_asin_result.html" 
    tables = [table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            # table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            ]
    keepaInfos = KeepaInfo.objects.values_list("asin_group_id").filter(account_id="user").distinct()
    choice_values = []
    for value in keepaInfos:
        choice_values.append((value[0], value[0]))

    def get(self, request, *args, **kwargs):
        # TODO ユーザー名チェック(URL直で打ったら他ユーザのチェックできない恐れあり)
        print(request.user)

        tables=[]
        table1 = None
        if "asin_group_id" in kwargs:
            args_asin_group_id = kwargs["asin_group_id"]
            table1 = table.KeepaInfoTable(KeepaInfo.objects.filter(
                account_id = request.user, asin_group_id = args_asin_group_id))
            table1.per_page_field = {"per_page": 1}
            # tables = [table1
            # # table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            # ]
        else:
            table1 = table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user"))
            # table1["per_page"] = self.per_page
            tables = [table1,
            # table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            ]

        form = SampleChoiceForm()
        form.fields['asin_group_id'].choices = self.choice_values

        context = self.get_context_data(**kwargs)
        context["form"] = form
        print("tables!!!!!!!!")
        # RequestConfig(request, paginate={'per_page': 3}).configure(table)
        # print(context["tables"][0].per_page_field[0])
        context["tables"][0] = table1
        context['aaaaa'] = "abbbb"
     

        print(context)
        return render(request, self.template_name, context)
        
        # return self.render_to_response(context)

        # return TemplateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # form = SampleChoiceForm(request.POST)
        asin_group_id = request.POST.get("asin_group_id", None)
        form = SampleChoiceForm(initial={"hidden_asin_group_id":asin_group_id })
        form.fields['asin_group_id'].choices = self.choice_values

        if asin_group_id :
            # args_asin_group_id = kwargs["asin_group_id"]
            tables = [table.KeepaInfoTable(KeepaInfo.objects.filter(
                account_id = request.user, asin_group_id = asin_group_id)),
            # table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            ]
        else:
            tables = [table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            # table.KeepaInfoTable(KeepaInfo.objects.filter(account_id="user")),
            ]
        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["tables"] = tables

        return render(request, self.template_name, context)
