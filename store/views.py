from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.pagination import PageNumberPagination



class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = ()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name', ]
    
    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StandardResultSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['price', 'category']
    search_fields = ['name', 'description']
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()
    pagination_class = StandardResultSetPagination
    
    def get_queryset(self):
        return Product.objects.filter(available=True)
    

    def get(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serilizer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
