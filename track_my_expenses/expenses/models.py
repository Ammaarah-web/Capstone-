from django.db import models
from django.contrib.auth.models import User

# Category model for expense categories
class Category(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name} ({self.user.username})"

# Expense model for tracking expenses
class Expense(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	date = models.DateField()
	notes = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.user.username} - {self.amount} on {self.date}"

# Create your models here.
