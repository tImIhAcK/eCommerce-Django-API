from django.conf import settings
from rest_framework.views import APIView
from django.shortcuts import redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from decimal import Decimal


import stripe

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self, request):
        order_id = request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        
        try:
            # Stripe checkout session data  
            session_data = {
				'mode': 'payment',
				'success_url': settings.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}',
				'cancel_url': settings.SITE_URL + '?canceled=true',
				'line_items': []
			}
            # add order items to the Stripe checkout session
            for item in order.items.all():
                session_data['line_items'].append({
					'price_data': {
						'unit_amount': int(item.price * Decimal('100')),
						'currency': 'usd',
						'product_data': {
							'name': item.product.name,
						},
					},
					'quantity': item.quantity,
				})
            # create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(**session_data)
            
            return redirect(checkout_session.url)
        except:
            return Response(
	        	{'error': 'Something went wrong when create stripe checkout session'},
	        	status=status.HTTP_500_INTERNAL_SERVER_ERROR
	        	)

	    
