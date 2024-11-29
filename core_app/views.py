from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from .models import Candle, Review
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ResetPasswordForm
from django.contrib.auth.decorators import login_required


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'core_app/login.html'   #custom login page template
    success_url = '/'              # redirected to homepage after login

class CustomLogoutView(LogoutView):
    next_page = '/logout/success/'                # redirected to homepage after logout

def logout_success(request):
    return render(request, 'core_app/logout_success.html', {'user' : request.user})

@login_required
def submit_review(request):

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if rating:
            review_data = Review.objects.create(
                user=request.user,
                review=review,
                rating=rating
            )
            review_data.save()

            return redirect('core_app:index')
        else:
            return HttpResponse('Invalid submission.', status=400)
    return HttpResponse('Invalid request', status=400)

def logout_without_review(request):
    logout(request)
    return redirect('core_app:index')

def index(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'core_app/index.html', {'cart_count': cart_count})


def about(request):
    return render(request, 'core_app/about.html')
