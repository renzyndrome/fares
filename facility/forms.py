from django import forms
from django.contrib.admin import widgets   
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

from .models import Facility, Reservation, Service

class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'


class ReservationForm(forms.ModelForm):
    services = forms.CharField(required=False)
    class Meta:
         model = Reservation
         fields = ['date', 'start_time', 'end_time', 'services']
         widgets = {
             'date': DatePickerInput(
           
             ), # default date-format %m/%d/%Y will be used
             'start_time': TimePickerInput(
                 options={
                     "format": "hh:mm A"
                 },
                 attrs={
                     'autocomplete': 'off'
                 }
             ).start_of('reservation time'),
             'end_time': TimePickerInput(
                 attrs={
                     'autocomplete': 'off'
                 }
             ).end_of('reservation time'),
         }

class CancellationForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['cancelation_note']