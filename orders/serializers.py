from rest_framework import serializers
from .models import Order, OrderItem
from .tasks import order_created
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']
        def validate(self, attrs):
            if attrs['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be a positive integer.")
            return attrs

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated', 'paid', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        # launch asynchronous task
        order_created.delay(order.id)

         # Add order.id to the session
        request = self.context.get('request')
        if request:
            session_key = request.session.session_key
            if session_key:
                session = Session.objects.get(session_key=session_key)
                session_data = session.get_decoded()
                session_data['order_id'] = order.id
                session.save()

        return order