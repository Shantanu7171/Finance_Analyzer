from django.urls import path
from .views import SubscriptionDetectionAPIView

urlpatterns = [
    path('', SubscriptionDetectionAPIView.as_view(), name='subscriptions'),
]
