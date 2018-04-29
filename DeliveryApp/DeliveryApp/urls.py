"""DeliveryApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^register/$', views.register, {'template_name': 'register.html'}, name='register'),
    url(r'^homepage/$', views.homepage, {'template_name': 'homepage.html'}, name='homepage'),
    url(r'^create_dish/$', views.create_dish, {'template_name': 'create_dish.html'}, name='create_dish'),
    url(r'^edit_dish/(?P<dish_id>[\w\-]+)/$', views.edit_dish, {'template_name': 'edit_dish.html'}, name='edit_dish'),
    url(r'^delete_dish/(?P<dish_id>[\w\-]+)/$', views.delete_dish, {'template_name': 'delete_dish.html'}, name='delete_dish'),
    url(r'^dish_detail/(?P<dish_id>[\w\-]+)/$', views.dish_detail, {'template_name': 'dish_detail.html'}, name='dish_detail'),
]
