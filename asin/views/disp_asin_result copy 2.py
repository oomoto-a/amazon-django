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

class ResultView(SingleTableView):
    model = KeepaInfo
    table_class = table.KeepaInfoTable
    table_pagination = {"per_page": 1}
    template_name = "asin/disp_asin_result.html" 

    # def get_context_data(self, **kwargs):
    #     context = super(ResultView, self).get_context_data(**kwargs)

    #     kinds = KeepaInfo.objects.all()
    #     context['table'] = table.KeepaInfoTable(kinds)
        
    #     return context

    def get_queryset(self):
        # デフォルトは全件取得
        results = self.model.objects.all()

        return results