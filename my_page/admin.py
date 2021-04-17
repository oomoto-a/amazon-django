from django.contrib import admin

# Register your models here.

from .models.account_info import AccountInfoModel
admin.site.register(AccountInfoModel)