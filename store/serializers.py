from rest_framework import serializers
from .models import Category, Product
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = serializers.SerializerMethodField()

    def get_image(self, product):
        return f"{settings.API_URL}{product.image.url}"

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description', 'image']