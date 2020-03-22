from django import forms
from .models import Facility

class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = '__all__'