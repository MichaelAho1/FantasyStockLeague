from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.ViewAllStocks.as_view(), name="viewAllStocks"),
]