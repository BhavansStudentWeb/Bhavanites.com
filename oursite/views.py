from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

def home(request):
    if request.user.is_authenticated:
        return render(request,'oursite/home.html')
    else:
        return HttpResponseRedirect('/login/')
def logout(request):
    return render(request,'registration/logout.html')