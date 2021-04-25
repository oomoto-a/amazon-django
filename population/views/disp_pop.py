from django.shortcuts import render
from django.views import generic
from django_tables2 import SingleTableView
from django.views.generic import ListView, UpdateView, DeleteView
from population.models import Population
from . import table
from asin.const import Const
import pandas as pd


class StatusView(SingleTableView):
    model = Population
    table_class = table.PopulationTable
    table_pagination = {"per_page":  Const.PAGE_PER_DEFAULT}
    template_name = "population/disp_pop.html"

    def get_queryset(self):

        # 年で絞る
        result = Population.objects.filter(year="2015")
            
        return result



