from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('stocks/', views.ViewAllStocks.as_view(), name="viewAllStocks"),
    path('owned-stocks/<uuid:league_id>/', views.ViewAllOwnedStocks.as_view(), name="viewAllOwnedStocks"),
]