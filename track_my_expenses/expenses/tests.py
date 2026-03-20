from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Expense, Category, Budget
import datetime


class ExpenseTrackerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category = Category.objects.create(
            name='Food',
            user=self.user
        )

    def test_add_expense(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_expense'), {
            'amount': '25.00',
            'category': self.category.id,
            'date': datetime.date.today(),
            'notes': 'Lunch'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 1)

        expense = Expense.objects.first()
        self.assertEqual(expense.amount, 25.00)
        self.assertEqual(expense.notes, 'Lunch')

    def test_edit_expense(self):
        self.client.login(username='testuser', password='testpass')
        expense = Expense.objects.create(
            user=self.user,
            amount=10.00,
            category=self.category,
            date=datetime.date.today(),
            notes='Breakfast'
        )

        response = self.client.post(reverse('edit_expense', args=[expense.id]), {
            'amount': '15.00',
            'category': self.category.id,
            'date': datetime.date.today(),
            'notes': 'Brunch'
        })

        self.assertEqual(response.status_code, 302)
        expense.refresh_from_db()
        self.assertEqual(expense.amount, 15.00)
        self.assertEqual(expense.notes, 'Brunch')

    def test_delete_expense(self):
        self.client.login(username='testuser', password='testpass')
        expense = Expense.objects.create(
            user=self.user,
            amount=5.00,
            category=self.category,
            date=datetime.date.today(),
            notes='Snack'
        )

        response = self.client.post(reverse('delete_expense', args=[expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 0)


class ExpenseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='modeluser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Transport',
            user=self.user
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Transport')
        self.assertEqual(self.category.user.username, 'modeluser')

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Transport (modeluser)')

    def test_expense_creation(self):
        expense = Expense.objects.create(
            user=self.user,
            amount=12.50,
            category=self.category,
            date=datetime.date.today(),
            notes='Bus fare'
        )

        self.assertEqual(expense.user, self.user)
        self.assertEqual(expense.amount, 12.50)
        self.assertEqual(expense.category, self.category)
        self.assertEqual(expense.notes, 'Bus fare')

    def test_expense_str_method(self):
        expense = Expense.objects.create(
            user=self.user,
            amount=20.00,
            category=self.category,
            date=datetime.date(2026, 3, 20),
            notes='Taxi'
        )

        self.assertEqual(str(expense), 'modeluser - 20.00 on 2026-03-20')

    def test_budget_creation(self):
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            monthly_limit=300.00
        )

        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.category, self.category)
        self.assertEqual(budget.monthly_limit, 300.00)

    def test_budget_str_method(self):
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            monthly_limit=500.00
        )

        self.assertEqual(str(budget), 'Transport - £500.00')