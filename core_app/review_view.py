from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Review
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ReviewView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core_app/review.html', {'user' : request.user})
    
    def post(self, request):
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
            return HttpResponseRedirect('/')
        else:
            logout(request)
            return HttpResponse('Invalid submission.', status=400)