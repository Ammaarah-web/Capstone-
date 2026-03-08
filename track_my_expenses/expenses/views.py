# Category report view for spending by category
from django.contrib.auth.decorators import login_required

@login_required
def category_report(request):
	expenses = Expense.objects.filter(user=request.user).order_by('-date')
	from collections import defaultdict
	category_totals = defaultdict(float)
	total_spending = 0.0
	for expense in expenses:
		if expense.category:
			category_totals[expense.category.name] += float(expense.amount)
			total_spending += float(expense.amount)
	categories = list(category_totals.keys())
	totals = list(category_totals.values())
	category_data = []
	for cat in categories:
		total = category_totals[cat]
		percent = round((total / total_spending) * 100, 2) if total_spending > 0 else 0
		category_data.append({'category': cat, 'total': total, 'percent': percent})
	return render(request, 'category_report.html', {
		'category_data': category_data,
	})
# Monthly report view for spending per month
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from datetime import datetime

from django.contrib.auth.decorators import login_required

# ...existing code...

@login_required
def monthly_report(request):
	import datetime
	year = request.GET.get('year', '2026')
	expenses = Expense.objects.filter(user=request.user, date__year=year)
	monthly = (
		expenses
		.annotate(month=TruncMonth('date'))
		.values('month')
		.annotate(total=Sum('amount'))
		.order_by('month')
	)
	monthly_labels = [item['month'].strftime('%b %Y') for item in monthly]
	monthly_data = [float(item['total']) for item in monthly]
	monthly_list = [
		{'label': label, 'total': total}
		for label, total in zip(monthly_labels, monthly_data)
	]
	# Get all years with expenses for dropdown
	all_years = Expense.objects.filter(user=request.user).dates('date', 'year')
	available_years = sorted(set([y.year for y in all_years]), reverse=True)
	return render(request, 'monthly_report.html', {
		'monthly_labels': monthly_labels,
		'monthly_data': monthly_data,
		'monthly_list': monthly_list,
		'selected_year': int(year),
		'available_years': available_years,
	})
# Calculate total spending per month and pass to dashboard.html
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from datetime import datetime

from django.contrib.auth.decorators import login_required

# ...existing code...

# Dashboard view: list user's expenses and monthly totals
@login_required
def dashboard(request):
	expenses = Expense.objects.filter(user=request.user).order_by('date')
	# Calculate totals per month
	monthly = (
		expenses
		.annotate(month=TruncMonth('date'))
		.values('month')
		.annotate(total=Sum('amount'))
		.order_by('month')
	)
	monthly_labels = [item['month'].strftime('%b %Y') for item in monthly]
	monthly_data = [float(item['total']) for item in monthly]
	return render(request, 'expenses/dashboard.html', {
		'expenses': expenses,
		'monthly_labels': monthly_labels,
		'monthly_data': monthly_data,
	})
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
	# Calculate totals per category
	from collections import defaultdict
	category_totals = defaultdict(float)
	total_spending = 0.0
	for expense in expenses:
		if expense.category:
			category_totals[expense.category.name] += float(expense.amount)
			total_spending += float(expense.amount)
	categories = list(category_totals.keys())
	totals = list(category_totals.values())
	# Build a combined list for template iteration
	category_data = []
	for cat in categories:
		total = category_totals[cat]
		percent = round((total / total_spending) * 100, 2) if total_spending > 0 else 0
		category_data.append({'category': cat, 'total': total, 'percent': percent})

	# Line chart dataset: spending over time
	date_totals = defaultdict(float)
	for expense in expenses:
		date_str = expense.date.strftime('%Y-%m-%d')
		date_totals[date_str] += float(expense.amount)
	date_labels = list(date_totals.keys())
	daily_totals = list(date_totals.values())

	return render(request, 'expenses/dashboard.html', {
		'expenses': expenses,
		'category_data': category_data,
		'total_spending': total_spending,
		'date_labels': date_labels,
		'daily_totals': daily_totals
	})

# Add expense view
@login_required
def add_expense(request):
	if request.method == 'POST':
		form = ExpenseForm(request.POST)
		if form.is_valid():
			expense = form.save(commit=False)
			expense.user = request.user
			expense.save()
			if 'save_add' in request.POST:
				return redirect('add_expense')
			else:
				return redirect('dashboard')
		else:
			# Show form with errors
			return render(request, 'add_expense.html', {'form': form})
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
