from django.urls import path
from .views import BankStatementUploadView

urlpatterns = [
    path('upload/', BankStatementUploadView.as_view(), name='bank_upload'),
]
