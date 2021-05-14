"""amazon_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_title = 'PriceMaster 管理画面' 
admin.site.site_header = 'PriceMaster 管理画面' 
admin.site.index_title = '設定変更'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('django.contrib.auth.urls')), #  追加
    path('', include("data_view.urls")), #  修正
    path('my_page/', include("my_page.urls")), 
    path('data_view/', include("data_view.urls")),  
    path('asin/', include("asin.urls")),
    path('population/', include("population.urls")),
    # path('account/', include("account.urls")),
]
