from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import SubscriptionService
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expenses.models import Expense

class SubscriptionDetectionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = SubscriptionService.detect_subscriptions(request.user)
        return Response({"subscriptions": subscriptions})

@login_required
def subscription_list_view(request):
    subscriptions = SubscriptionService.detect_subscriptions(request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})

@login_required
def subscription_detail_view(request):
    desc = request.GET.get('description', '')
    amount = request.GET.get('amount')
    category = request.GET.get('category')

    expenses = Expense.objects.filter(
        user=request.user,
        description=desc,
        amount=amount,
        category=category
    ).order_by('-date')

    context = {
        'description': desc if desc else f"Recurring {category.title()} Expense",
        'amount': amount,
        'category': category,
        'expenses': expenses
    }
    return render(request, 'subscriptions/subscription_detail.html', context)
