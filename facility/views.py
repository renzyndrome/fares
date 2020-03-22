from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Facility
from .forms import FacilityForm

# Create your views here.
@login_required
def facilities(request):
    facilities = Facility.objects.all()
    context = {
        'facilities': facilities,
    }
    return render(request, 'facility/facility_list.html', context)

@login_required
def facility(request):
    return render(request, 'facility/facilty.html')

@login_required
def facility(request, facility_id):
    facility = Facility.objects.get(pk=facility_id)
    if request.method == 'POST':
        p_form = FacilityForm(request.POST, request.FILES,
                                    instance=facility)
    
        if p_form.is_valid():
            p_form.save()
            #messages.success(request, f'Your account has been updated!')
            return redirect('facility', facility_id=facility_id)
    else:
        p_form = FacilityForm(instance=facility)
    context = {
        'p_form': p_form
    }

    return render(request, 'facility/facility.html', context)
