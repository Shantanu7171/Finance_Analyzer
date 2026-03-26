from django.db.models import Count
from expenses.models import Expense

class SubscriptionService:
    @staticmethod
    def detect_subscriptions(user):
        recurring = Expense.objects.filter(
            user=user
        ).values(
            'description', 'amount', 'category'
        ).annotate(
            count=Count('id')
        ).filter(count__gte=2).order_by('-count')

        subscriptions = []
        for item in recurring:
            name = item['description'].strip() if item['description'] else f"Recurring {item['category'].title()} Expense"
            subscriptions.append({
                'name': name,
                'amount': item['amount'],
                'category': item['category'],
                'occurrences': item['count'],
                'is_subscription': True,
                'raw_description': item['description']
            })
        return subscriptions
