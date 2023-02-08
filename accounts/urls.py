from .views import RegisterAPI, LoginAPI
from django.urls import path
from knox import views as knox_views
from . import views

app_name = "accounts"


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('nse_demo/', views.nse_demo, name = 'nse_demo'),
    path('home/', views.home, name = 'home'),
]