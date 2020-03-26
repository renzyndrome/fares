from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Facility, Service
from users.models import Profile
from .forms import FacilityForm, ReservationForm


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
        services = Service
        r_form = ReservationForm(request.POST)
        if r_form.is_valid():
            reserve = r_form.save(commit=False)
            reserve.user = user
            reserve.facility = facility
            # reserve.services.add()
            reserve.total_amount = facility_rate
            reserve.save()
            return redirect('/')
    else:
        r_form = ReservationForm()
    context = {
        'r_form': r_form,
    }

    return render(request, 'facility/reserve.html', context)
