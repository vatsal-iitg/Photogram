from django.shortcuts import render
from .import forms

# Create your views here.
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    form = forms.SignUpForm()
    return render(request, 'sign_up.html',{
        'form': form
    })