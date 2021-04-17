from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib import messages



# ASIN設定画面
class Manual(generic.TemplateView):
    template_name = "data_view/manual.html"

    def get(self, request, *args, **kwargs):
        return render(request,  self.template_name)



