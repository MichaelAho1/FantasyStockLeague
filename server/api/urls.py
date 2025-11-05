from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.ViewAllStocks.as_view(), name="viewAllStocks"),
    path('owned-stocks/<uuid:league_id>/', views.ViewAllOwnedStocks.as_view(), name="viewAllOwnedStocks"),
]