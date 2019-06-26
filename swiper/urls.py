
from django.conf.urls import url,include
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect



urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url('^api/users/',include('user.urls')),


]
