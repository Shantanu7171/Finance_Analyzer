from rest_framework import viewsets, permissions
from .models import Income
from .serializers import IncomeSerializer

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import IncomeForm

class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'incomes'

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income-list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'income/income_confirm_delete.html'
    success_url = reverse_lazy('income-list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)
