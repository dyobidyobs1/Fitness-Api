from django.urls import re_path, path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView




urlpatterns = [
    re_path('login', views.login),
    re_path('register', views.register),
    re_path('test_token', views.test_token),
    re_path('get_exercise', views.exercise),
    re_path('profile', views.profile),
    re_path('history', views.history),
    re_path('leaderboards', views.leaderboards),
    re_path('plan/<str:pk>', views.plangenerate),

    re_path('stats', views.stats),
    re_path('schema', SpectacularAPIView.as_view(), name='schema'),
    re_path('docs', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    
    ]
