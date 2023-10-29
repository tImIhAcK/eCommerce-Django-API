from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CategoryList(APIView):
    authentication_classes = ()
    permission_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', ]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProductList(APIView):
    authentication_classes = ()
    permission_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price', 'category']
    paginate_by=30

    def get(self, request):
        products = Product.objects.filter(available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
