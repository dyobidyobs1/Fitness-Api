from django.urls import re_path, path
from . import views



urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('test_token', views.test_token),
    re_path('get_exercise', views.exercise),
    re_path('profile', views.profile),
    re_path('history', views.history),

    re_path('stats', views.stats),
    
    ]
