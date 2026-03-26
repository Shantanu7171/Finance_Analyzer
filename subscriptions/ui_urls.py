from django.urls import path
from .views import subscription_list_view, subscription_detail_view

urlpatterns = [
    path('', subscription_list_view, name='subscription-list'),
    path('detail/', subscription_detail_view, name='subscription-detail'),
]
