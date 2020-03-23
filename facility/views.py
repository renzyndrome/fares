from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Facility
from .forms import FacilityForm

# Create your views here.



def facility(request):
    facilities = Facility.objects.all()
    context = {
        'facilities': facilities,
    }
    return render(request, 'facility/facility_list.html', context)


@login_required
def facility_detail(request, facility_id):
    facility = Facility.objects.get(pk=facility_id)
    context = {
        'facility':facility
    }

    return render(request, 'facility/facility.html', context)
