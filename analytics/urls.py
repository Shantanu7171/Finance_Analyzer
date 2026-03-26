from django.urls import path
from .views import DashboardAPIView, RecommendationAPIView

urlpatterns = [
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    path('recommendations/', RecommendationAPIView.as_view(), name='recommendations'),
]
