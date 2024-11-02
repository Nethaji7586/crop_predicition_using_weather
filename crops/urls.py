from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('register/', views.register, name='register'),  # User registration
    path('', views.suggest_crops, name='suggest_crops'),  # Crop suggestions view
    path('historical-data/', views.historical_data_view, name='historical_data'),  # Historical data view
    path('crop-trends/', views.crop_trends_view, name='crop_trends'),  # Crop trends view
    path('market-rates/', views.market_rates_view, name='market_rates'),  # Market rates view
]
