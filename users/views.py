from django.shortcuts import render, redirect
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, BalanceForm
from .models import Profile
from .decorators import unauthenticated_user, allowed_users, admin_only


def home(request):
	return render(request, 'index.html')

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        # user_profile 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.is_active = True
            # register.first_name = form.cleaned_data.get('first_name')
            # register.last_name = form.cleaned_data.get('last_name')
            register.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form} )


@login_required
def profile(request):
    if request.method == 'POST': 
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                    instance=request.user.profile)
    
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def view_user(request, user_id):
    request.POST._mutable = True
    user_profile = Profile.objects.get(pk=user_id)
    user = user_profile.user
    if request.method == 'POST': 
        #u_form = UserUpdateForm(request.POST, instance=user)
        if(request.user.profile.role == 'Cashier'):
            p_form = BalanceForm(request.POST, request.FILES,
                                    instance=user_profile)
            new_value = [Decimal(p_form.data['additional_balance']) ,Decimal(p_form.data['balance'])]
            p_form.data['balance'] = sum(new_value)
        else:
            p_form = ProfileUpdateForm(request.POST, request.FILES,
                                    instance=user_profile)
    
        #if u_form.is_valid() and p_form.is_valid():
        if p_form.is_valid():
            #u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('view_user', user_id=user_id)
    else:
        #u_form = UserUpdateForm(instance=user)
        if(request.user.profile.role == 'Cashier'):
            p_form = BalanceForm(instance=user_profile)
        else:
            p_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user': user,
        #'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def user_list(request):
    user_list = Profile.objects.all()
    context = {
        'user_list': user_list,
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_detail(request, user_id):
    user = get_object_or_404(Profile, pk=user_id)
    return render(request, 'users/')
