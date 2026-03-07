
from django.contrib import admin
from .models import Expense, Category

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'user')

# Admin for Expense
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('user', 'amount', 'category', 'date')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
