from django.shortcuts import render, redirect
from ..forms import ChangeUserInfo
from django.contrib import messages
from django.views import View
from ..models import OrderItem


class InfoChangeView(View):
    def get(self, request):
        return render(request, 'core_app/my_profile/personal_details.html', {'user': request.user})
    
    def post(self, request):
        form = ChangeUserInfo(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been updated.")
            return redirect('core_app:details')
        return render(request, 'core_app/my_profile/personal_details.html', {'user': request.user})


class BillingPayments(View):
    def get(self, request):
        return render(request, 'core_app/my_profile/billing.html')
    

class Settings(View):
    def get(self, request):
        return render(request, 'core_app/my_profile/settings.html')
    

class TransactionsHistory(View):
    def get(self, request):
        order_items = OrderItem.objects.filter(order__user=request.user)

        return render(request, 'core_app/my_profile/transactions.html', {
            'details' : order_items,
            "order_length" : len(order_items)
            })