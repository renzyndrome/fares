from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
import datetime as dt
from django.conf import settings

from .models import Facility, Service, Reservation, Gallery
from users.models import Profile
from .forms import FacilityForm, ReservationForm, CancellationForm
from users.decorators import admin_only

from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum, Count


def facility(request):
    facilities = Facility.objects.all()
    context = {
        'facilities': facilities,
    }
    return render(request, 'facility/facility_list.html', context)


def facility_detail(request, facility_id):
    facility = Facility.objects.get(pk=facility_id)
    reservation_list = Reservation.objects.filter(facility=facility.id).order_by('start_time')
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
def reserve(request, facility_id):
    reservations = Reservation.objects.filter(facility__id=facility_id)
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
            
            if facility.isVehicle:
                cart = [facility.rate]
            else:
                cart = [(facility.rate * duration)]

            services = Service.objects.filter(id__in=request.POST.getlist('services'))
            for service in services:
                cart.append(service.price)            
            if r_form.cleaned_data['add_half_hour']:
                reserve.end_time += timedelta(minutes= 30)
                cart.append(facility.rate/2)

            reserve.total_amount = sum(cart)

            schedule = Reservation.objects.filter(Q(start_time__range=[start_time, reserve.end_time])|
                                                  Q(end_time__range=(start_time,reserve.end_time))|
                                                  Q(start_time__lt=start_time, end_time__gt=reserve.end_time)).filter(facility=facility)
            
            if schedule:    # reservation checking
                messages.warning(request, 'Reservation Unsuccessful: The time and date you choose was taken')

            else:
                if user.balance >= reserve.total_amount:
                    user.balance -= reserve.total_amount

                    r_form.save()
                    r_form.save_m2m()
                    user.save()

                    # notify via email

    
                    try:
                        context = {
                            'user': user,
                            'reservation': reserve

                        }
                        html_content = render_to_string('users/reservation_email.html', context)
                        send_mail(
                        'RESERVATION DETAILS',
                        strip_tags(html_content),
                        'dlsudfacility@gmail.com',
                        [request.user.email],
                        fail_silently=False,
                        )
                    except Exception as e:
                        print(e)
                        e
                        return redirect('home')

                    messages.success(request,'reserved successfully')
                    return redirect('user_reservation_list')

                else:
                    messages.warning(request, 'Reservation Unsuccessful: Insuficient Account Balance')
        else:
            messages.error(request, "Error")         
    else:
        r_form = ReservationForm()
    r = dir(r_form)
    context = {
        'r_form': r_form,
        'r': r,
        'reservations': reservations
    }

    return render(request, 'facility/reserve.html', context)



@login_required
def user_reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user.profile)

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
    reservation = Reservation.objects.get(pk=reservation_id)
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