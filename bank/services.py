import pandas as pd
from decimal import Decimal
from expenses.models import Expense
from income.models import Income

class BankStatementParser:
    @staticmethod
    def parse_and_categorize(file_obj, user):
        try:
            df = pd.read_csv(file_obj)
        except Exception as e:
            return {"error": f"Failed to parse CSV: {str(e)}"}

        df.columns = df.columns.str.title()
        
        required_cols = {'Date', 'Description', 'Amount'}
        if not required_cols.issubset(set(df.columns)):
            return {"error": f"Missing required columns. Found: {list(df.columns)}. Expected: {list(required_cols)}"}

        incomes_created = 0
        expenses_created = 0

        for index, row in df.iterrows():
            desc = str(row['Description']).strip()
            amount = Decimal(str(row['Amount']))
            date_str = pd.to_datetime(row['Date']).date()

            if amount > 0:
                Income.objects.create(
                    user=user,
                    source=desc,
                    amount=amount,
                    date=date_str
                )
                incomes_created += 1
            elif amount < 0:
                abs_amount = abs(amount)
                category = BankStatementParser.categorize_expense(desc)
                Expense.objects.create(
                    user=user,
                    category=category,
                    amount=abs_amount,
                    date=date_str,
                    description=desc
                )
                expenses_created += 1

        return {
            "success": True,
            "incomes_added": incomes_created,
            "expenses_added": expenses_created
        }

    @staticmethod
    def categorize_expense(description):
        desc = description.lower()
        if any(word in desc for word in ['restaurant', 'mcdonalds', 'grocery', 'food', 'supermarket', 'pizza', 'eats']):
            return 'food'
        if any(word in desc for word in ['uber', 'lyft', 'gas', 'transit', 'train', 'bus', 'station']):
            return 'transport'
        if any(word in desc for word in ['electric', 'water', 'internet', 'rent', 'insurance', 'bill']):
            return 'bills'
        if any(word in desc for word in ['movie', 'netflix', 'spotify', 'game', 'concert', 'cinema']):
            return 'entertainment'
        
        return 'shopping'
