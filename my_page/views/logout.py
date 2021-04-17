from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.views import generic

class LogoutView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        logout(request)
