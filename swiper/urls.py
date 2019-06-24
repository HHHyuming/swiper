
from django.conf.urls import url,include
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login(request):
    return HttpResponse("LOING")
def register(request):
    if request.method=='GET':
        return render(request,'index.html')
    return redirect('/login/')


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url('^api/users/',include('user.urls')),
    url('^login/',login),
    url('^register/',register),

]
