from django.shortcuts import render
from django.views import generic
from django_tables2 import SingleTableView
from django.views.generic import ListView, UpdateView, DeleteView
from asin.models.asin_group_id import AsinGroupId
from . import table
from asin.const import Const

class StatusView(SingleTableView):
    model = AsinGroupId
    table_class = table.AsinGroupIdTable
    table_pagination = {"per_page":  Const.PAGE_PER_DEFAULT}
    template_name = "asin/disp_asin_status.html"

    def get_queryset(self):

        # アカウントで絞る
        info_count = "".join(["SELECT COUNT(*) FROM asin_keepainfo ",
                " WHERE asin_asingroupid.account_id = asin_keepainfo.account_id ",
                " AND asin_asingroupid.asin_group_id = asin_keepainfo.asin_group_id"])
        result = AsinGroupId.objects.filter(account_id=self.request.user).extra(select={'count': info_count})
            
        return result



