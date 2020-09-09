from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import stripe

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'User':
			return redirect('home')

		if group == 'Admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function

def create_payment(request, user_cart):
	
	
	total = (user_cart.total_amount)*100
	stripe.api_key = 'sk_test_51HK4L4HQE5VBqI7fhgUH8jaSxQHUBXZ0xqm6OJIj3esd6915SRLaPlNBUALEzPAZV0JJlAultthLk3oqP3jCReXG00Q2t9UbvX'

	if request.method=="POST":
		print(total)
		data = json.loads(request.body)
		# Create a PaymentIntent with the order amount and currency
		intent = stripe.PaymentIntent.create(
			amount=total,
			currency=data['currency'],
			metadata={'integration_check': 'accept_a_payment'},
			)
		try:
			return JsonResponse({'publishableKey':	
				'pk_test_51HK4L4HQE5VBqI7fOWxKON42Rdi1KlAPZJPmsqMSpBsEpey6jnstG9kP96UlVvCq3WX0MFPGwFc3bgpoRm0AtiZw00DsUzZK5o', 'clientSecret': intent.client_secret})
		except Exception as e:
			return JsonResponse({'error':str(e)},status= 403)