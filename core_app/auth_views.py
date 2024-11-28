from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Candle, Review
from .forms import RegistrationForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View

class LoginView(LoginView):
    template_name = 'core_app/auth/login.html'
    success_url = '/'

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'core_app/auth/registration.html', {'form': form}) 

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('core_app:login')
        return render(request, 'core_app/auth/registration.html', {'form': form})

class ResetPasswordView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, "core_app/auth/reset_password.html", {"form": form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            new_password = form.cleaned_data["new_password"]

            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(new_password)  
                user.save()  
                messages.success(request, "Password reset successfully!")
                return redirect("core_app:login")  
            except User.DoesNotExist:
                messages.error(request, "No user found with the given username and email!")
                return redirect("core_app:reset_password")
        return render(request, "core_app/auth/reset_password.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/logout/success')

def logout_success(request):
    return render(request, 'core_app/logout_success.html', {'user' : request.user})