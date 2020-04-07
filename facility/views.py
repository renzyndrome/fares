from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Q



from .models import Facility, Service, Reservation
from users.models import Profile
from .forms import FacilityForm, ReservationForm, CancellationForm


def facility(request):
    facilities = Facility.objects.all()
    context = {
        'facilities': facilities,
    }
    return render(request, 'facility/facility_list.html', context)


def facility_detail(request, facility_id):
    facility = Facility.objects.get(pk=facility_id)
    tags = facility.tags.all()
    context = {
        'facility':facility,
        'tags': tags
    }

    return render(request, 'facility/facility.html', context)



@login_required
def reserve(request, facility_id):
    if request.method == 'POST':
        facility = Facility.objects.get(pk=facility_id)
        facility_rate = facility.rate
        user = Profile.objects.get(user=request.user.id)
        r_form = ReservationForm(request.POST)
        if r_form.is_valid():
            
            reserve = r_form.save(commit=False)
            reserve.user = user
            reserve.facility = facility
            duration = r_form.cleaned_data['duration']
            # end_time = datetime.now().strftime('%I:%M %p')
          
            start_time = r_form.cleaned_data['start_time']
         
            reserve.end_time = start_time + timedelta(hours= duration)
            cart = [(facility.rate * duration)]

            services = Service.objects.filter(pk=request.POST.get('services'))
            for service in services:
                cart.append(service.price)            
            if r_form.cleaned_data['add_half_hour']:
                reserve.end_time += timedelta(minutes= 30)
                cart.append(facility.rate/2)

            reserve.total_amount = sum(cart)

            schedule = Reservation.objects.filter(Q(start_time__range=[start_time, reserve.end_time])|
                                                  Q(end_time__range=(start_time,reserve.end_time))|
                                                  Q(start_time__lt=start_time, end_time__gt=reserve.end_time))

            if schedule:    # reservation checking
                return redirect('already_reserved')

            if user.balance >= reserve.total_amount:
                user.balance -= reserve.total_amount
                         
                r_form.save()
                r_form.save_m2m()
                user.save()
                return redirect('reservation_list')

            else:
                return redirect('insufficient_balance')
        else:
            r_form # wip error msg           
    else:
        r_form = ReservationForm()
    r = dir(r_form)
    context = {
        'r_form': r_form,
        'r': r,
    }

    return render(request, 'facility/reserve.html', context)

@login_required
def cancellation_request_list(request):
    role = request.user.profile.role
    reservations = Reservation.objects.filter(status='PENDING FOR CANCELLATION')

    if request.method == 'POST':
        form = Reservation.objects.get(pk=request.POST.get('reservation'))    
        form.status = 'CANCELLED'
        form.save()
        return redirect('/')
    
    context = {
        'reservations': reservations,
        'role': role
    }

    return render(request, 'facility/cancellation_request_list.html', context)

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user.profile)
    for reservation in reservations:
        if reservation.status == 'CANCELLED':
            reservation.delete()
    context = {
        'reservations': reservations
    }

    return render(request, 'facility/reservation_list.html', context)

@login_required
def insufficient_balance(request):
    return HttpResponse('Insufficient balance!')

@login_required
def already_reserved(request):
    return HttpResponse('Sorry, this facility has already reserved! Please choose another time.')




def cancellation_request(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    if request.method == 'POST':
        c_form = CancellationForm(request.POST, request.FILES,
                                    instance=reservation)
        if c_form.is_valid():

            total_amount = request.POST.get('total_amount')
            user = Profile.objects.get(user=request.user.id)

            form = c_form.save(commit=False)
            form.status = 'PENDING FOR CANCELLATION'
            user.balance += reservation.total_amount
            form.save()
            user.save()
            return redirect('reservation_list')
        
    else:
        c_form = CancellationForm()
        
    context = {
        'c_form': c_form,
        'reservation': reservation
    }
    return render(request, 'facility/cancellation.html', context)

