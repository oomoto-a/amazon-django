from django.shortcuts import render
from django.views import generic
from django_tables2 import SingleTableView
from django.views.generic import ListView, UpdateView, DeleteView
from population.models import Population
from . import table
from asin.const import Const

import matplotlib
#バックエンドを指定
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import numpy as np
# from asin.models.keepa_info import KeepaInfo
import datetime
import japanize_matplotlib
import seaborn as sns
from cycler import cycler



class PlotAsin(generic.TemplateView):
    template_name = "population/disp_pop_plot.html"
    form_class = "PlotForm"
    def get(self, request, id, *args, **kwargs):
        required = ""

        params={
            "id":id,
            "account_id": "request.user",
            "title": "人口グラフ",
            "required": required,
            # "form": form
        }
        return render(request, self.template_name, params)

