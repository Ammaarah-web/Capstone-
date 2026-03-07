from django import forms
from .models import Expense, Category

# Form for Expense model
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'notes']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('Amount must be positive.')
        return amount

# Form for Category model
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
