"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from forum import views


urlpatterns = [
    path("admin/", admin.site.urls),
    #auth
    path('signup/', views.signupuser, name="signupuser"),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('login/', views.loginuser, name="loginuser"),

    #forum
    path('forum/', views.forummain, name="forummain"),
    path('', views.home, name="home"),
    path('create/', views.createthread, name="createthread"),
    path('forum/<int:thread_pk>', views.viewthread, name="viewthread"),
    path('edit/<int:thread_pk>', views.editthread, name="editthread"),
    path('forum/<int:thread_pk>/delete', views.deletethread, name="deletethread"),
]
