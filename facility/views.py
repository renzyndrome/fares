from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
        services = Service.objects.all()
        r_form = ReservationForm(request.POST)
        if r_form.is_valid():
            try:
                reserve = r_form.save(commit=False)
                reserve.user = user
                reserve.facility = facility


                cart = [facility.rate]
                for service in reserve.services.all():
                    cart.append(service.price)

                
                reserve.total_amount = sum(cart)
                if user.balance >= reserve.total_amount:                    
                    reserve.save()
                    return redirect('reservation_list')
            except:
                return redirect('facility_list')
            
    else:
        r_form = ReservationForm()
    r = dir(r_form)
    services = Service.objects.all()
    context = {
        'r_form': r_form,
        'r': r,
        'my_services': services
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

def cancellation_request(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    if request.method == 'POST':
        c_form = CancellationForm(request.POST, request.FILES,
                                    instance=reservation)
        if c_form.is_valid():
            form = c_form.save(commit=False)
            form.status = 'PENDING FOR CANCELLATION'
            form.save()
            return redirect('reservation_list')
        
    else:
        c_form = CancellationForm()
        
    context = {
        'c_form': c_form,
        'reservation': reservation
    }
    return render(request, 'facility/cancellation.html', context)

