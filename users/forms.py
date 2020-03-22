from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name']

class BalanceForm(forms.ModelForm):
    additional_balance = forms.DecimalField(max_digits=10, decimal_places=2)
    balance = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'True'}), max_digits=10, decimal_places=2)
    class Meta:
        model = Profile
        fields = ['image', 'balance']
    
    def save(self, commit=True):
        return super(BalanceForm, self).save(commit=commit)

