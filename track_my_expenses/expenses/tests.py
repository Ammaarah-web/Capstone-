from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Expense, Category
from django.urls import reverse
import datetime

class ExpenseTrackerTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.category = Category.objects.create(name='Food', user=self.user)

			'amount': '25.00',
			'category': self.category.id,
			'date': datetime.date.today(),
			'notes': 'Lunch'
		})
		self.assertEqual(response.status_code, 302)  # Redirect after add
		self.assertEqual(Expense.objects.count(), 1)
		expense = Expense.objects.first()
		self.assertEqual(expense.amount, 25.00)
		self.assertEqual(expense.notes, 'Lunch')

	def test_edit_expense(self):
		self.client.login(username='testuser', password='testpass')
		expense = Expense.objects.create(user=self.user, amount=10.00, category=self.category, date=datetime.date.today(), notes='Breakfast')
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
		expense = Expense.objects.create(user=self.user, amount=5.00, category=self.category, date=datetime.date.today(), notes='Snack')
		response = self.client.post(reverse('delete_expense', args=[expense.id]))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Expense.objects.count(), 0)
