from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q



def is_admin(user):
    if not user.is_staff:
        raise PermissionDenied("You don't have permission to access this page.")
    return True

@user_passes_test(is_admin)
@login_required
def login(request):
    return render(request, 'submit/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            if form.cleaned_data.get('user_type') == 'service_provider':
                # Redirect to the first post page for service providers
                return redirect(reverse('post-create'))
            else:
                # Redirect to login for regular users
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'submit/register.html', {'form': form})


def is_admin(user):
    if not user.is_staff:
        raise PermissionDenied("You don't have permission to access this page.")
    return True

@user_passes_test(is_admin)
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}

    return render(request, 'submit/profile.html', context)

    #CleanilinessSol2024
