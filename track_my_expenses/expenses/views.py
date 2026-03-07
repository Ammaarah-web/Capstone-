from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

class HomePage(TemplateView):
	"""
	Displays home page
	"""
	template_name = 'index.html'

# User registration view

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm

# Dashboard view: list user's expenses
@login_required
def dashboard(request):
	expenses = Expense.objects.filter(user=request.user).order_by('-date')
	return render(request, 'dashboard.html', {'expenses': expenses})

# Add expense view
@login_required
def add_expense(request):
	if request.method == 'POST':
		form = ExpenseForm(request.POST)
		if form.is_valid():
			expense = form.save(commit=False)
			expense.user = request.user
			expense.save()
			return redirect('dashboard')
	else:
		form = ExpenseForm()
	return render(request, 'add_expense.html', {'form': form})

# Edit expense view
@login_required
def edit_expense(request, expense_id):
	expense = get_object_or_404(Expense, id=expense_id, user=request.user)
	if request.method == 'POST':
		form = ExpenseForm(request.POST, instance=expense)
		if form.is_valid():
			form.save()
			return redirect('dashboard')
	else:
		form = ExpenseForm(instance=expense)
	return render(request, 'edit_expense.html', {'form': form, 'expense': expense})

# Delete expense view
@login_required
def delete_expense(request, expense_id):
	expense = get_object_or_404(Expense, id=expense_id, user=request.user)
	if request.method == 'POST':
		expense.delete()
		return redirect('dashboard')
	return render(request, 'delete_expense.html', {'expense': expense})
