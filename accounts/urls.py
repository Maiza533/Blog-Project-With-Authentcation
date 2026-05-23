from django.contrib import admin
from django.urls import path
from .views import create_blog, delete_blog, blog_detail, edit_blog, blog_list, login_view, logout_view, profile, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('create/', create_blog, name='create_blog'),
    path('edit/<slug:slug>/', edit_blog, name='edit_blog'),
    path('delete/<slug:slug>/', delete_blog, name='delete_blog'),
    path('profile/', profile, name='profile')
]