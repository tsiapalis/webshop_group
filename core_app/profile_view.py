from django.shortcuts import render, redirect
from .forms import ChangeUserInfo
from django.contrib.auth.models import User
from django.views import View



class InfoChangeView(View):
    def get(self, request):
        form = ChangeUserInfo()
        return render(request, 'core_app/my_profile/personal_details.html', {'form': form}) 


class BillingPayments(View):
    def get(self, request):
        return render(request, 'core_app/my_profile/billing.html')
    

class Settings(View):
    def get(self, request):
        return render(request, 'core_app/my_profile/settings.html')
    

class TransactionsHistory(View):
    def get(self, request):
        return render(request, 'core_app/my_profile/transactions.html')