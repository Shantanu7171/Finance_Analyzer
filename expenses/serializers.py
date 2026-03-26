from rest_framework import serializers
from .models import Expense, Budget

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ('user',)
        
    def validate_monthly_limit(self, value):
        if value < 0:
            raise serializers.ValidationError("Budget limit cannot be negative.")
        return value
