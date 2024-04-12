from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer

# Create your views here.

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    