from django.urls import path
from .views import bank_upload_view

urlpatterns = [
    path('upload/', bank_upload_view, name='bank-upload'),
]
