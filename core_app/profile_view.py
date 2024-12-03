from django.shortcuts import render, redirect
from .forms import ChangeUserInfo
from django.contrib import messages
from django.views import View
from .models import Order, Item, OrderItem



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

        orders = [order for order in Order.objects.all() if order.user.username == request.user.username]

        details = {}
        for detail in OrderItem.objects.all():
            if detail.order in orders:
                details[detail.item] = detail.quantity
        for detail in details:
            print(detail, details[detail])

        return render(request, 'core_app/my_profile/transactions.html', {
            'details' : details,
            "order_length" : len(details)
            })
