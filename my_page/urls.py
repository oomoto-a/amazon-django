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
from django.urls import path
from django.urls import path, include
from .views.logout import LogoutView
from .views.mypage import MypageView
from .views.billing import BillingView,redirect_view

app_name="my_page"
urlpatterns = [
    path('', MypageView.as_view(), name="mypage"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('billing/', BillingView.as_view(), name="billing"),
    path('redirect/', redirect_view, name="redirectpage"),
]
