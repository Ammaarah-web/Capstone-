# Homepage view
def homepage(request):
	return render(request, 'index.html')
# Edit budget view
def edit_budget(request, budget_id):
	budget = get_object_or_404(Budget, id=budget_id, user=request.user)
	if request.method == 'POST':
		form = BudgetForm(request.POST, instance=budget)
		if form.is_valid():
			form.save()
			return redirect('budgets')
	else:
		form = BudgetForm(instance=budget)
	return render(request, 'add_budget.html', {'form': form, 'edit_mode': True})

# Delete budget view
def delete_budget(request, budget_id):
	budget = get_object_or_404(Budget, id=budget_id, user=request.user)
	if request.method == 'POST':
		budget.delete()
		return redirect('budgets')
	return render(request, 'delete_expense.html', {'object': budget, 'type': 'budget'})
# User registration view
# Budgets view


# All imports at the top
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Budget, Expense
from .forms import ExpenseForm, BudgetForm
# Add budget view
def add_budget(request):
	if request.method == 'POST':
		form = BudgetForm(request.POST)
		if form.is_valid():
			budget = form.save(commit=False)
			budget.user = request.user
			budget.save()
			return redirect('budgets')
	else:
		form = BudgetForm()
	return render(request, 'add_budget.html', {'form': form})
from collections import defaultdict
from datetime import date, datetime


# Budgets view

from django.contrib.auth.decorators import login_required

@login_required
def budgets(request):
	user_budgets = Budget.objects.filter(user=request.user)
	budget_data = []
	from decimal import Decimal
	for budget in user_budgets:
		today = date.today()
		spent = Expense.objects.filter(
			user=request.user,
			category=budget.category,
			date__year=today.year,
			date__month=today.month
		).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
		monthly_limit = budget.monthly_limit if budget.monthly_limit else Decimal('0.00')
		percent_used = float((spent / monthly_limit) * 100) if monthly_limit > 0 else 0
		progress = min(percent_used, 100)
		budget_data.append({
			'id': budget.id,
			'category': budget.category.name,
			'monthly_limit': float(monthly_limit),
			'total_spent': float(spent),
			'percent_used': percent_used,
			'progress': progress
		})
	return render(request, 'budgets.html', {'budgets': budget_data})


# Category report view for spending by category

def category_report(request):
	from datetime import date
	selected_month = request.GET.get('month')
	current_year = date.today().year
	expenses = Expense.objects.filter(user=request.user).order_by('-date')
	if selected_month:
		expenses = expenses.filter(date__month=int(selected_month), date__year=current_year)
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

	# Summary statistics
	highest_category = None
	highest_total = 0.0
	if category_totals:
		highest_category = max(category_totals, key=category_totals.get)
		highest_total = category_totals[highest_category]
	num_categories = len(categories)

	category_labels = categories
	category_totals = totals
	return render(request, 'category_report.html', {
		'category_data': category_data,
		'total_spending': total_spending,
		'highest_category': highest_category,
		'highest_total': highest_total,
		'num_categories': num_categories,
		'category_labels': category_labels,
		'category_totals': category_totals,
	})


# Monthly report view for spending per month

from django.contrib.auth.decorators import login_required

@login_required
def monthly_report(request):
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


# Dashboard view: list user's expenses and monthly totals

def dashboard(request):
	expenses = Expense.objects.filter(user=request.user).order_by('-id')
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

	from decimal import Decimal
	user_budgets = Budget.objects.filter(user=request.user)
	# Calculate total budget and total spent
	total_budget = user_budgets.aggregate(total=Sum('monthly_limit'))['total'] or Decimal('0.00')
	total_spent = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
	remaining_budget = total_budget - total_spent
	spent_percent = float((total_spent / total_budget) * 100) if total_budget > 0 else 0
	remaining_percent = float((remaining_budget / total_budget) * 100) if total_budget > 0 else 0

	# Line chart dataset: daily spending totals
	from django.db.models.functions import TruncDate
	daily = (
		expenses
		.annotate(day=TruncDate('date'))
		.values('day')
		.annotate(total=Sum('amount'))
		.order_by('day')
	)
	chart_dates = [item['day'].strftime('%b %d') for item in daily]
	chart_totals = [float(item['total']) for item in daily]

	return render(request, 'expenses/dashboard.html', {
		'expenses': expenses,
		'monthly_labels': monthly_labels,
		'monthly_data': monthly_data,
		'total_budget': total_budget,
		'total_spent': total_spent,
		'remaining_budget': remaining_budget,
		'spent_percent': spent_percent,
		'remaining_percent': remaining_percent,
		'chart_dates': chart_dates,
		'chart_totals': chart_totals,
	})




# Add expense view

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

def delete_expense(request, expense_id):
	expense = get_object_or_404(Expense, id=expense_id, user=request.user)
	if request.method == 'POST':
		expense.delete()
		return redirect('dashboard')
	return render(request, 'delete_expense.html', {'expense': expense})
