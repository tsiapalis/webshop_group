from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import Review, Candle
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

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

            logout(request)
            return redirect('core_app:index')
        else:
            logout(request)
            return HttpResponse('Invalid submission.', status=400)
    logout(request)
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
