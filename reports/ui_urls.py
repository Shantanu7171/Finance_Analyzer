from django.urls import path
from .views import report_view, MonthlyReportAPIView

urlpatterns = [
    path('', report_view, name='report-generator'),
    path('monthly/', MonthlyReportAPIView.as_view(), name='monthly-report'),
]
