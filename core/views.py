

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .import forms
from django.views import View
from django.contrib.auth.decorators import login_required
from core import forms
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def sign_up(request):
    form = forms.SignUpForm()

    if request.method=='POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()

            user  = form.save(commit=False)
            user.username=email
            user.save()

            login(request,user)
            return redirect('/socialfeed') # redirecting to the social feed 

    return render(request, 'core/sign_up.html',{
        'form': form
    })

@login_required()
def profile_page(request):
    user_form = forms.BasicUserForm(instance=request.user)
    profile_data_form = forms.BasicProfileForm(instance=request.user.userprofile)
    password_form = PasswordChangeForm(request.user,request.POST)
    if request.method == "POST":
        if request.POST.get('action') == 'update_password':
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request,user)

                messages.success(request, 'Your password has been updated')
                return redirect(reverse('profile'))

        if request.POST.get('action') == 'update_profile':
            user_form = forms.BasicUserForm(request.POST, instance=request.user)
            profile_data_form = forms.BasicProfileForm(request.POST,request.FILES,instance=request.user.userprofile)
            if user_form.is_valid() and profile_data_form.is_valid():
                user_form.save()
                profile_data_form.save()
                messages.success(request, 'Your profile has been updated')
                return redirect(reverse('profile'))
        
    return render(request,'core/profile.html',{
            "user_form": user_form,
            "profile_data_form": profile_data_form,
            "password_form": password_form
    })