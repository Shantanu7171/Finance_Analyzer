from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from expenses.models import Expense
from income.models import Income
from django.db.models import Sum
from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

from subscriptions.services import SubscriptionService

class MonthlyReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.today()
        year = int(request.query_params.get('year', today.year))
        month = int(request.query_params.get('month', today.month))

        user = request.user

        income_agg = Income.objects.filter(user=user, date__year=year, date__month=month).aggregate(total=Sum('amount'))
        total_income = income_agg['total'] or Decimal('0.00')

        expense_qs = Expense.objects.filter(user=user, date__year=year, date__month=month)
        expense_agg = expense_qs.aggregate(total=Sum('amount'))
        total_expenses = expense_agg['total'] or Decimal('0.00')

        savings = total_income - total_expenses

        breakdown = expense_qs.values('category').annotate(total=Sum('amount')).order_by('-total')
        top_category = breakdown[0]['category'] if breakdown else 'None'
        top_category_amount = breakdown[0]['total'] if breakdown else Decimal('0.00')

        # Detect subscriptions for the report
        all_subs = SubscriptionService.detect_subscriptions(user)
        # Filter subscriptions that have expenses in this specific month
        monthly_subs = []
        sub_total = Decimal('0.00')
        for sub in all_subs:
            # Check if any expense for this sub exists in the given month/year
            if Expense.objects.filter(
                user=user, date__year=year, date__month=month,
                description=sub['raw_description'], amount=sub['amount']
            ).exists():
                monthly_subs.append(sub)
                sub_total += Decimal(str(sub['amount']))

        data = {
            'year': year,
            'month': month,
            'total_income': str(total_income),
            'total_expenses': str(total_expenses),
            'savings': str(savings),
            'top_spending_category': top_category,
            'top_spending_amount': str(top_category_amount),
            'subscriptions': monthly_subs,
            'subscription_total': str(sub_total)
        }

        export_format = request.query_params.get('output_format', 'json')
        if export_format.lower() == 'pdf':
            return self.generate_pdf(data, user)

        return Response(data)

    def generate_pdf(self, data, user):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, f"Monthly Financial Report: {data['month']}/{data['year']}")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 710, f"User: {user.email}")
        p.drawString(100, 680, f"Total Income: ₹{data['total_income']}")
        p.drawString(100, 650, f"Total Expenses: ₹{data['total_expenses']}")
        p.drawString(100, 620, f"Savings: ₹{data['savings']}")
        
        p.drawString(100, 580, f"Top Spending Category: {data['top_spending_category'].title()}")
        p.drawString(100, 550, f"Amount Spent on Top Category: ₹{data['top_spending_amount']}")

        # Subscription Section in PDF
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, 510, "Detected Monthly Subscriptions:")
        p.setFont("Helvetica", 10)
        y_pos = 490
        if data['subscriptions']:
            for sub in data['subscriptions']:
                p.drawString(120, y_pos, f"- {sub['name']}: ₹{sub['amount']} ({sub['category'].title()})")
                y_pos -= 20
            p.drawString(100, y_pos - 10, f"Subscription Total: ₹{data['subscription_total']}")
        else:
            p.drawString(120, y_pos, "No recurring subscriptions identified this month.")

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{data["year"]}_{data["month"]}.pdf"'
        return response

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def report_view(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    years = range(current_year - 5, current_year + 1)
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    return render(request, 'reports/report_generator.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
        'current_month': current_month
    })
