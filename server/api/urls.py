from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('stocks/', views.ViewAllStocks.as_view(), name="viewAllStocks"),
    path('owned-stocks/<uuid:league_id>/', views.ViewAllOwnedStocks.as_view(), name="viewAllOwnedStocks"),
    path('weekly-profits/<uuid:league_id>/', views.ViewUserWeeklyProfits.as_view(), name="ViewUserWeeklyProfits"),
    path('opponent-weekly-profits/<uuid:league_id>/', views.ViewOpponentWeeklyProfits.as_view(), name="ViewOpponentWeeklyProfits"),
    path('leagues/', views.ViewAllLeagues.as_view(), name="leagues"),
]