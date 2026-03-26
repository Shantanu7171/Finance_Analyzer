"""
URL configuration for finance_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import register_view
from analytics.views import dashboard_view

from django.views.generic import RedirectView

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=True)),
    path('register/', RedirectView.as_view(url='/accounts/register/', permanent=True)),
    path('accounts/register/', register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/auth/', include(('accounts.urls', 'accounts'), namespace='api')),
    path('expenses/', include('expenses.ui_urls')),
    path('income/', include('income.ui_urls')),
    path('subscriptions/', include('subscriptions.ui_urls')),
    path('bank/', include('bank.ui_urls')),
    path('reports/', include('reports.ui_urls')),
    path('api/expenses/', include(('expenses.urls', 'expenses'), namespace='api-expenses')),
    path('api/income/', include(('income.urls', 'income'), namespace='api-income')),
    path('api/analytics/', include(('analytics.urls', 'analytics'), namespace='api-analytics')),
    path('api/subscriptions/', include(('subscriptions.urls', 'subscriptions'), namespace='api-subscriptions')),
    path('api/bank/', include(('bank.urls', 'bank'), namespace='api-bank')),
    path('api/reports/', include(('reports.urls', 'reports'), namespace='api-reports')),
]
