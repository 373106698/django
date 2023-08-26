"""Data_Check URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from app01 import views

urlpatterns = [
    path("index/", views.index),

    #用户管理
    path("user/", views.user),
    path("user_add/", views.user_add),
    path("user_del/", views.user_del),
    #正则表达式传递参数
    path("user/<int:nid>/edit/", views.user_edit),

    path("depart/", views.depart),
    path("depart/add/", views.depart_add),
    path("depart/del/", views.depart_del),

    #正则表达式传递参数
    path("depart/<int:nid>/edit/", views.depart_edit),

]
