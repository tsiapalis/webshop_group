from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from forms import RegistrationForm

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'core_app/login.html'   #custom login page template
    success_url = '/'              # redirected to homepage after login

class CustomLogoutView(LogoutView):
    next_page = '/'                # redirected to homepage after logout


def index(request):
    return render(request, 'core_app/index.html')

def about(request):
    return render(request, 'core_app/about.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'core_app/register.html', {'form': form})

