"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    path('', index, name="index"),
    path('admin/', admin.site.urls, name="admin"),

    path('accounts/logIn/', logIn, name="logIn"),
    path('accounts/signUp/', signUp, name="signUp"),
    path('accounts/logOut/', logOut, name="logOut"),
    path('accounts/profile/', updateProfilePicture, name='updateProfilePicture'),
    
    path('authenticate/newUser/', authenticateUser, name="authenticateUser"),
    
    path('myCart/', viewCart, name="viewCart"),

    path('addToCart/', viewCart, name="addToCart"),

    path('products/<str:product>', products, name="products"),

    path('builder', builder, name="builder")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)