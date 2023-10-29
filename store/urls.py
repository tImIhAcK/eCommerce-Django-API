from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
]
