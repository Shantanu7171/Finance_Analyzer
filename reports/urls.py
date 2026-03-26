from django.urls import path
from .views import MonthlyReportAPIView

urlpatterns = [
    path('monthly/', MonthlyReportAPIView.as_view(), name='monthly_report'),
]
