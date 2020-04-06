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
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), required=False)
    # add_half_hour = forms.BooleanField(required=False)

    class Meta:
         model = Reservation
         fields = ['date', 'start_time', 'duration', 'add_half_hour', 'services',  ]
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