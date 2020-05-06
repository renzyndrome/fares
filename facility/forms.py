from django import forms
from django.contrib.admin import widgets   
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime as dt
import pytz

from .models import Facility, Reservation, Service

class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = '__all__'



class ReservationForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), required=False)
    # add_half_hour = forms.BooleanField(required=False)

    def clean_start_time(self):
        utc=pytz.UTC

        start_time = self.cleaned_data['start_time']
        if start_time.replace(tzinfo=utc) < dt.now().replace(tzinfo=utc):
            raise forms.ValidationError("The date cannot be in the past!")
        return start_time
    

    class Meta:
        model = Reservation
        fields = [ 'start_time', 'duration', 'add_half_hour', 'services',  ]
        widgets = {

        'start_time': DateTimePickerInput()
        }


    
    def __init__(self, *args, **kwargs):
        self.services = kwargs.pop('Service', None)
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields["services"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["services"].labels = "sample"
        self.fields["services"].help_text = '<br>*Additional fees will be added upon adding services'
        self.fields["services"].queryset = Service.objects.all()
        self.fields["add_half_hour"].widget = forms.widgets.CheckboxInput()

    def user_balance(self):
        user_profile = Profile.objects.get(user=request.user.id)
        balance = user_profile.balance
        total_amount = self.cleaned_data['total_amount']
        if balance < total_amount:
            raise forms.ValidationError("insuficient balance")
        return total_amount



class CancellationForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['cancellation_note']