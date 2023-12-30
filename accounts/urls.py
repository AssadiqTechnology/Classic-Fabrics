# accounts/urls.py
from django.urls import path
from .views import register_view, login_view, forgot_password, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('logout/', logout_view, name='logout'),
]
