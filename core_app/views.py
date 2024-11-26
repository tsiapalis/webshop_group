from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from .models import Candle
from .forms import RegistrationForm

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'core_app/login.html'   #custom login page template
    success_url = '/'              # redirected to homepage after login

class CustomLogoutView(LogoutView):
    next_page = '/logout/success/'                # redirected to homepage after logout

def logout_success(request):
    return render(request, 'core_app/logout_success.html')

def submit_review(request):
    if request.method == 'POST':
        review = request.POST.get('review')
        # Save or process the review as needed
        return HttpResponse('Thank you for your review!')
    return HttpResponse('Invalid request', status=400)


def index(request):
    return render(request, 'core_app/index.html')

def discovery(request):
    items = Candle.objects.all()
    return render(request, 'core_app/discovery.html', {'items': items})

def about(request):
    return render(request, 'core_app/about.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'core_app/registration.html', {'form': form})

