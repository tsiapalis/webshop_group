from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'core_app/login.html'   #custom login page template
    success_url = '/'              # redirected to homepage after login

class CustomLogoutView(LogoutView):
    next_page = '/'                # redirected to homepage after logout

    
def index(request):
    return render(request, 'core_app/index.html')
