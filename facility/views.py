from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.decorators import create_payment
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from django.http import JsonResponse
import datetime as dt
from django.conf import settings
from itertools import chain
from .models import Facility, Service, Vehicle, FacilityReservation, VehicleReservation, Gallery
from users.models import Profile
from .forms import FacilityForm, FacilityReservationForm, VehicleReservationForm, CancellationForm
from users.decorators import admin_only

from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum, Count


@login_required
def facility(request):
    facilities = Facility.objects.all()
    context = {
        'facilities': facilities,
    }
    return render(request, 'facility/facility_list.html', context)

@login_required
def facility_detail(request, facility_id):
    facility = Facility.objects.get(pk=facility_id)
    reservation_list = FacilityReservation.objects.filter(facility=facility.id).order_by('start_time')
    gallery = Gallery.objects.filter(facility=facility.id)

    tags = facility.tags.all()
    context = {
        'facility':facility,
        'tags': tags,
        'reservation_list': reservation_list,
        'gallery':gallery
    }

    return render(request, 'facility/facility.html', context)

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'facility/vehicle_list.html', context)

@login_required
def vehicle_detail(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    reservation_list = VehicleReservation.objects.filter(vehicle=vehicle.id).order_by('start_time')
    # gallery = Gallery.objects.filter(vehicle=vehicle.id)

 
    context = {
        'vehicle':vehicle,
        # 'tags': tags,
        'reservation_list': reservation_list,
        # 'gallery':gallery
    }

    return render(request, 'facility/vehicle.html', context)


@login_required
def reserve_facility(request, facility_id):

    facility = Facility.objects.get(pk=facility_id)
    reservations = FacilityReservation.objects.filter(facility=facility)
    r_form = FacilityReservationForm(facility)
    r = dir(r_form)

    if request.method == 'POST':
        
        facility_rate = facility.rate
        user = Profile.objects.get(user=request.user.id)
        r_form = FacilityReservationForm(facility, request.POST)
  
        if user.facilityreservation_set.filter(status="PENDING PAYMENT").exists():
            messages.warning(request, 'Unpaid reservation found')
            return redirect('user_facility_reservation_list')
        else:
            if r_form.is_valid():
                
                reserve = r_form.save(commit=False)
                reserve.user = user
                reserve.facility = facility
                duration = r_form.cleaned_data['duration']
                start_time = r_form.cleaned_data['start_time']
                reserve.end_time = start_time + timedelta(hours= duration)
                
                cart = [(facility.rate * duration)]

                services = Service.objects.filter(id__in=request.POST.getlist('services'))
                for service in services:
                    cart.append(service.price)
                half_hour_price = 0            
                if r_form.cleaned_data['add_half_hour']:
                    reserve.end_time += timedelta(minutes= 30)
                    half_hour_price = facility.rate/2
                    cart.append(half_hour_price)
                    print(half_hour_price)
                total = sum(cart)
                reserve.total_amount = sum(cart)
                reserve.status = 'PENDING PAYMENT'
                schedule = FacilityReservation.objects.filter(Q(start_time__range=[start_time, reserve.end_time])|
                                                    Q(end_time__range=(start_time,reserve.end_time))|
                                                    Q(start_time__lt=start_time, end_time__gt=reserve.end_time)).filter(facility=facility)
                
                if schedule:    # reservation checking
                    messages.warning(request, 'Reservation Unsuccessful: The time and date you choose was taken')
                    return redirect('home')
                else:
                    r_form.save()
                    r_form.save_m2m()
                
                context = {'user': user,
                            'facility': facility,
                            'services': services,
                            'half_hour_price': half_hour_price,
                            'total': total}

                return render(request, 'facility/checkout.html', context)         
  
            else:
                messages.error(request, "Error")

    context = {
        'r_form': r_form,
        'reservations': reservations
    }

    return render(request, 'facility/reserve_facility.html', context)

@login_required
def reserve_vehicle(request, vehicle_id):

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    reservations = VehicleReservation.objects.filter(vehicle=vehicle)
    r_form = VehicleReservationForm(vehicle)
    r = dir(r_form)

    if request.method == 'POST':
        
        vehicle_rate = vehicle.rate
        user = Profile.objects.get(user=request.user.id)
        r_form = VehicleReservationForm(vehicle, request.POST)
  
        if user.vehiclereservation_set.filter(status="PENDING PAYMENT").exists():
            messages.warning(request, 'Unpaid reservation found')
            return redirect('user_reservation_list')
        else:
            if r_form.is_valid():
                
                reserve = r_form.save(commit=False)
                reserve.user = user
                reserve.vehicle = vehicle
                duration = r_form.cleaned_data['duration']
                start_time = r_form.cleaned_data['start_time']
                reserve.end_time = start_time + timedelta(days= duration)
                print(reserve.end_time)
                
                cart = [(vehicle.rate * duration)]

                services = Service.objects.filter(id__in=request.POST.getlist('services'))
                for service in services:
                    cart.append(service.price)            

                total = sum(cart)
                reserve.total_amount = sum(cart)
                reserve.status = 'PENDING PAYMENT'
                schedule = VehicleReservation.objects.filter(Q(start_time__range=[start_time, reserve.end_time])|
                                                    Q(end_time__range=(start_time,reserve.end_time))|
                                                    Q(start_time__lt=start_time, end_time__gt=reserve.end_time)).filter(vehicle=vehicle)
                
                if schedule:    # reservation checking
                    messages.warning(request, 'Reservation Unsuccessful: The time and date you choose was taken')
                    return redirect('home')
                else:
                    r_form.save()
                    r_form.save_m2m()
                
                context = {'user': user,
                            'vehicle': vehicle,
                            'reservation': r_form,
                            'total': total}

                return render(request, 'facility/checkout_vehicle_reservation.html', context)         
  
            else:
                messages.error(request, "Error")

    context = {
        'r_form': r_form,
        'reservations': reservations
    }

    return render(request, 'facility/reserve_vehicle.html', context)


@login_required
@csrf_exempt
def facility_create_payment(request):
    user = Profile.objects.get(user=request.user.id)
    user_cart = user.facilityreservation_set.last()
    # create_payment(request,user_cart)
    total = (user_cart.total_amount)*100
    stripe.api_key = 'sk_test_51HK4L4HQE5VBqI7fhgUH8jaSxQHUBXZ0xqm6OJIj3esd6915SRLaPlNBUALEzPAZV0JJlAultthLk3oqP3jCReXG00Q2t9UbvX'

    if request.method=="POST":
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

    return render(request, 'facility/checkout.html')

@login_required
@csrf_exempt
def vehicle_create_payment(request):
    user = Profile.objects.get(user=request.user.id)
    user_cart = user.vehiclereservation_set.last()
    # create_payment(request,user_cart)
    total = (user_cart.total_amount)*100
    stripe.api_key = 'sk_test_51HK4L4HQE5VBqI7fhgUH8jaSxQHUBXZ0xqm6OJIj3esd6915SRLaPlNBUALEzPAZV0JJlAultthLk3oqP3jCReXG00Q2t9UbvX'

    if request.method=="POST":
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

    return render(request, 'facility/checkout_vehicle_reservation.html')

@login_required
def pay_with_funds(request):
    user = Profile.objects.get(user=request.user.id)
    reservation = user.facilityreservation_set.last()
    
    if user.balance >= reservation.total_amount:
                    user.balance -= reservation.total_amount
                    reservation.status = 'SUCCESS'
                    reservation.save()
                    user.save()
                    # notify via email    
                    send_email(request.user, reservation)

                    messages.success(request,'reserved successfully')
    else:
        messages.error(request,'insufficient funds')
    return redirect('user_reservation_list')

@login_required
def vehicle_pay_with_funds(request):
    user = Profile.objects.get(user=request.user.id)
    reservation = user.vehiclereservation_set.last()
    
    if user.balance >= reservation.total_amount:
                    user.balance -= reservation.total_amount
                    reservation.status = 'SUCCESS'
                    reservation.save()
                    user.save()
                    # notify via email    
                    send_email(request.user, reservation)

                    messages.success(request,'reserved successfully')
                    print(reservation.status)
    else:
        messages.error(request,'insufficient funds')
    return redirect('user_reservation_list')

def send_email(user, reservation):
    try:
        context = {
            'user': user,
            'reservation': reservation
        }
        html_content = render_to_string('users/reservation_email.html', context)
        send_mail(
        'RESERVATION DETAILS',
        strip_tags(html_content),
        'dlsudfacility@gmail.com',
        [user.email],
        fail_silently=False,
        )
    except Exception as e:
        print(e)
        e
        return redirect('home')


@login_required
def facility_payment_complete(request):
    user = Profile.objects.get(user=request.user.id)
    reservation = user.facilityreservation_set.last()
    if request.method=="POST":
        data = json.loads(request.POST.get("payload"))
        if data["status"] == "succeeded":
			# save purchase here/ setup email confirmation
            reservation.status = "SUCCESS"
            reservation.save()
            print(reservation.status)
            # notify via email    
            send_email(request.user, reservation)

    return redirect('user_reservation_list')


@login_required
def vehicle_payment_complete(request):
    user = Profile.objects.get(user=request.user.id)
    reservation = user.vehiclereservation_set.last()
    if request.method=="POST":
        data = json.loads(request.POST.get("payload"))
        if data["status"] == "succeeded":
			# save purchase here/ setup email confirmation
            reservation.status = "SUCCESS"
            reservation.save()
            # notify via email    
            send_email(request.user, reservation)

    return redirect('user_reservation_list')


@login_required
def user_reservation_list(request):
    reservations = chain(FacilityReservation.objects.filter(user=request.user.profile), VehicleReservation.objects.filter(user=request.user.profile))

    context = {
        'reservations': reservations
    }

    return render(request, 'facility/user_reservation_list.html', context)


@login_required
def user_facility_reservation_list(request):
    reservations = FacilityReservation.objects.filter(user=request.user.profile)

    context = {
        'reservations': reservations
    }

    return render(request, 'facility/user_reservation_list.html', context)
    


def reservation_list(request):
    reservations = Reservation.objects.all()

    if request.method == 'POST':
        form = Reservation.objects.get(pk=request.POST.get('reservation'))    
        user = Profile.objects.get(user=form.user.id)
        user.balance += form.total_amount
        user.save()
        form.delete()

    context = {
        'reservations': reservations,
    }

    return render(request, 'facility/reservation_list.html', context)

@login_required
def insufficient_balance(request):
    return HttpResponse('Insufficient balance!')

@login_required
def already_reserved(request):
    return HttpResponse('Sorry, this facility has already reserved! Please choose another time.')



def cancellation_request(request, reservation_id):
    reservation = FacilityReservation.objects.get(pk=reservation_id)
    if request.method == 'POST':
        c_form = CancellationForm(request.POST, request.FILES,
                                    instance=reservation)
        if c_form.is_valid():

            total_amount = request.POST.get('total_amount')
            user = Profile.objects.get(user=request.user.id)

            form = c_form.save(commit=False)
            form.status = 'PENDING FOR CANCELLATION'
            form.save()
            return redirect('user_reservation_list')
        
    else:
        c_form = CancellationForm()
        
    context = {
        'c_form': c_form,
        'reservation': reservation
    }
    return render(request, 'facility/cancellation.html', context)

def vehicle_cancellation_request(request, reservation_id):
    reservation = VehicleReservation.objects.get(pk=reservation_id)
    if request.method == 'POST':
        c_form = CancellationForm(request.POST, request.FILES,
                                    instance=reservation)
        if c_form.is_valid():

            total_amount = request.POST.get('total_amount')
            user = Profile.objects.get(user=request.user.id)

            form = c_form.save(commit=False)
            form.status = 'PENDING FOR CANCELLATION'
            form.save()
            return redirect('user_reservation_list')
        
    else:
        c_form = CancellationForm()
        
    context = {
        'c_form': c_form,
        'reservation': reservation
    }
    return render(request, 'facility/cancellation.html', context)

def approve_cancellation(request, reservation_id):
    reservation = FacilityReservation.objects.get(pk=reservation_id)
    requestor = reservation.user
    requestor.balance += reservation.total_amount
    reservation.status = 'CANCELLED'
    requestor.save()
    reservation.save()
    return redirect('admin_reservation_list')

def facility_approve_cancellation(request, reservation_id):
    reservation = VehicleReservation.objects.get(pk=reservation_id)
    requestor = reservation.user
    requestor.balance += reservation.total_amount
    reservation.status = 'CANCELLED'
    requestor.save()
    reservation.save()
    return redirect('admin_reservation_list')


@login_required
def weekly_income(request):
    income_list = (Reservation.objects
        .annotate(year=ExtractYear('start_time'))
        .annotate(week=ExtractWeek('start_time'))
        .values('year', 'week')
        .annotate(income=Sum('total_amount'))
    )
    weekly_list = []
    
    for income in income_list:
        if income['week']:
            week = "{year}-W{week}-1".format(year=income['year'], week=income['week'])
            timestamp = dt.datetime.strptime(week, "%Y-W%W-%w")
            d = str(income['year']) + "-W" + str(income['week'])            
            start = dt.datetime.strptime(d  + '-1', '%G-W%V-%u')
            income['week'] = dt.datetime.strftime(start,'%b %d, %Y')
            income['end_week'] =dt.datetime.strftime(start +  dt.timedelta(days=6),'%b %d, %Y')
            income['income'] = str(income['income'])


    context = {
        'income_list': income_list,
    }   

    
    return render(request, 'facility/income.html', context)