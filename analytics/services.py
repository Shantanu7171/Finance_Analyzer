from decimal import Decimal
from django.db.models import Sum
from income.models import Income
from expenses.models import Expense

class AnalyticsService:
    @staticmethod
    def get_dashboard_data(user):
        income_agg = Income.objects.filter(user=user).aggregate(total=Sum('amount'))
        total_income = income_agg['total'] or Decimal('0.00')

        expense_agg = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))
        total_expenses = expense_agg['total'] or Decimal('0.00')

        savings = total_income - total_expenses
        
        savings_rate = Decimal('0.00')
        if total_income > Decimal('0.00'):
            savings_rate = (savings / total_income) * Decimal('100.00')

        breakdown = Expense.objects.filter(user=user).values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')

        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'savings': savings,
            'savings_rate': round(savings_rate, 2),
            'expense_breakdown': list(breakdown)
        }

    @staticmethod
    def get_recommendations(user):
        data = AnalyticsService.get_dashboard_data(user)
        total_income = data['total_income']
        savings_rate = data['savings_rate']
        expense_breakdown = data['expense_breakdown']

        recommendations = []

        if total_income == Decimal('0.00'):
            recommendations.append("You have no recorded income. Consider adding income sources to start analyzing your finances.")
            return recommendations

        if savings_rate < Decimal('20.00'):
            recommendations.append(f"Your savings rate is {savings_rate}%. A good rule of thumb is to save at least 20% of your income.")

        for expense in expense_breakdown:
            category = expense['category']
            amount = expense['total']
            percentage = (amount / total_income) * Decimal('100.00')

            if category == 'food' and percentage > Decimal('30.00'):
                recommendations.append("Food expenses are high (>30% of income). Consider cooking more meals at home to reduce costs.")
            elif category == 'entertainment' and percentage > Decimal('15.00'):
                recommendations.append("Entertainment expenses are high (>15% of income). Look for lower-cost or free leisure activities.")
            elif category == 'shopping' and percentage > Decimal('20.00'):
                recommendations.append("Shopping expenses account for >20% of your income. Consider adhering to a stricter budget for discretionary items.")

        if not recommendations:
            recommendations.append("Great job! Your spending is well-balanced and within healthy limits.")

        return recommendations
