from django.urls import path
from .views import IncomeListView, IncomeCreateView, IncomeUpdateView, IncomeDeleteView

urlpatterns = [
    path('', IncomeListView.as_view(), name='income-list'),
    path('add/', IncomeCreateView.as_view(), name='income-add'),
    path('<int:pk>/edit/', IncomeUpdateView.as_view(), name='income-edit'),
    path('<int:pk>/delete/', IncomeDeleteView.as_view(), name='income-delete'),
]
