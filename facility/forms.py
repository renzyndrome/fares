from django import forms
from django.contrib.admin import widgets   
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime as dt
import pytz

from .models import Facility, FacilityReservation, VehicleReservation, Service

class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = '__all__'



class FacilityReservationForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), required=False)
    # add_half_hour = forms.BooleanField(required=False)

    def clean_start_time(self):
        utc=pytz.UTC

        start_time = self.cleaned_data['start_time']
        if start_time.replace(tzinfo=utc) < dt.now().replace(tzinfo=utc):
            raise forms.ValidationError("The date cannot be in the past!")
        return start_time
    

    class Meta:
        model = FacilityReservation
        fields = [ 'start_time', 'duration', 'services', 'add_half_hour' ]
        widgets = {

        'start_time': DateTimePickerInput()
        }


    
    def __init__(self, facility, *args, **kwargs):
        self.services = kwargs.pop('Service', None)
        super(FacilityReservationForm, self).__init__(*args, **kwargs)
        self.fields["services"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["services"].labels = "sample"
        self.fields["services"].help_text = '<br>*Additional fees will be added upon adding services'
        self.fields["services"].queryset = Service.objects.filter(facility=facility)
        self.fields["add_half_hour"].widget = forms.widgets.CheckboxInput()

class VehicleReservationForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), required=False)
    # add_half_hour = forms.BooleanField(required=False)


    

    class Meta:
        model = VehicleReservation
        fields = ['vehicle', 'department', 'driver', 'num_passengers', 'start_time', 'duration', 'starting_place', 'destination', 'purpose']
        widgets = {

        'start_time': DateTimePickerInput()
        }

    def __init__(self, vehicle, *args, **kwargs):
        self.services = kwargs.pop('Service', None)
        super(VehicleReservationForm, self).__init__(*args, **kwargs)
        self.fields["services"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["services"].labels = "sample"
        self.fields["services"].help_text = '<br>*Additional fees will be added upon adding services'
        self.fields["services"].queryset = Service.objects.filter(vehicle=vehicle)
    
    def clean_start_time(self):
        utc=pytz.UTC

        start_time = self.cleaned_data['start_time']
        if start_time.replace(tzinfo=utc) < dt.now().replace(tzinfo=utc):
            raise forms.ValidationError("The date cannot be in the past!")
        return start_time
class CancellationForm(forms.ModelForm):
    
    class Meta:
        model = FacilityReservation
        fields = ['cancellation_note']