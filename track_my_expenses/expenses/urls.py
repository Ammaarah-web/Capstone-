from django.urls import path

from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('monthly/', views.monthly_report, name='monthly_report'),
    path('category/', views.category_report, name='category_report'),
    path('budgets/', views.budgets, name='budgets'),
    path('add_budget/', views.add_budget, name='add_budget'),
    path('edit_budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
]