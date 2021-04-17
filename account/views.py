from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import *
from my_page.models.account_info import *

# Create your views here.

class SignupView(FormView):
    form_class = MyUserCreateForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('data_view:manual')
    def form_valid(self, form):
        form.save()
        # 認証
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        # AccountInfoModelへの追加
        AccountInfoModel(login_user_name=form.cleaned_data['username'],
                         login_user_email=form.cleaned_data['email']).save()

        
        # ログイン
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)