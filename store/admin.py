from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']
	# prepolulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'available', 'created', 'updated']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'available']
	search_fields = ['name']
	# prepolulated_fields = {'slug': ('name',)}

