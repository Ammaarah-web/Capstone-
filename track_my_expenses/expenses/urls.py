from django.views.generic import RedirectView

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page=None), name='logout'),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('monthly/', views.monthly_report, name='monthly_report'),
    path('category/', views.category_report, name='category_report'),
]
