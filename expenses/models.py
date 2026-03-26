from django.db import models
from django.conf import settings

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('shopping', 'Shopping'),
        ('bills', 'Bills'),
        ('entertainment', 'Entertainment'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.amount}"

from django.core.validators import MinValueValidator
from decimal import Decimal

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=50, choices=Expense.CATEGORY_CHOICES)
    monthly_limit = models.DecimalField(
        max_digits=12, decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'category'], name='unique_user_budget_category')
        ]

    def __str__(self):
        return f"{self.user} - {self.category} Budget: {self.monthly_limit}"
