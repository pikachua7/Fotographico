from django.contrib import admin
from django.urls import path
from .views import gallery,viewPhoto,addPhoto,registerPage,loginPage,logoutUser,homePage

urlpatterns = [
    path('',homePage,name='home'),
    # path('',loginPage,name='login'),
    path('register/',registerPage,name='register'),
    path('login/',loginPage,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('home/<int:user_id>', gallery,name='gallery'),
    path('photo/<str:pk>/',viewPhoto,name='photo'),
    path('add/',addPhoto,name="add"),
]
