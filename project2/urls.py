"""project2 URL Configuration

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
from django.urls import path
from app.views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('logout',LogoutView.as_view(next_page='/'),name='logout'),
    path('about',about,name='about'),


    #<-----Admin URLs----->

    path('admin_login',admin_login,name='admin_login'),
    path('admin_home',admin_home,name='admin_home'),
    path('admin_profile', admin_profile, name='admin_profile'),
    path('change_password_admin', change_password_admin, name='change_password_admin'),

    path('admin_approve_visitor', admin_approve_visitor,name='admin_approve_visitor'),
    path('approve_visitor', approve_visitor, name='approve_visitor'),
    path('delete_visitor', delete_visitor, name='delete_visitor'),

    path('admin_add_admin', admin_add_admin, name='admin_add_admin'),
    path('admin_active_admin', admin_active_admin,name='admin_active_admin'),
    path('delete_admin_active', delete_admin_active, name='delete_admin_active'),

    path('admin_active_visitor', admin_active_visitor,name='admin_active_visitor'),
    path('delete_visitor_active', delete_visitor_active, name='delete_visitor_active'),

    #<-----Visitor URLs----->

    path('visitor_signup',visitor_signup,name='visitor_signup'),
    path('visitor_login',visitor_login,name='visitor_login'),
    path('visitor_home',visitor_home,name='visitor_home'),
    path('visitor_profile', visitor_profile, name='visitor_profile'),
    path('change_password_visitor', change_password_visitor, name='change_password_visitor'),

    path('visitor_find_crop',visitor_find_crop, name='visitor_find_crop'),

    path('api/predict-crop/', predict_crop_api, name='predict_crop_api'),

    path('admin-signup/', views.admin_signup, name='admin_signup'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)