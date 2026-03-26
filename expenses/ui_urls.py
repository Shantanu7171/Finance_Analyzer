from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView,
    BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView
)

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('add/', ExpenseCreateView.as_view(), name='expense-add'),
    path('<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense-edit'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('budgets/add/', BudgetCreateView.as_view(), name='budget-add'),
    path('budgets/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget-edit'),
    path('budgets/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget-delete'),
]
