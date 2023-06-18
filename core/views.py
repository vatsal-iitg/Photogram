from django.shortcuts import render, redirect
from django.contrib.auth import login
from .import forms

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