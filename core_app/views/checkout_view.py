from django.views import View
from django.shortcuts import render, get_object_or_404
from ..models import Candle
from django.http import HttpResponseRedirect

class DetailsView(View):
    def get(self, request):
        cart = request.session.get('cart', {})    
        
        subTotal = 0
        items = []
        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)

            if item.in_stock == 0:
                # Skip items if out of stock
                continue

            if quantity > item.in_stock:
                # Change quantity to match the available stock
                quantity = item.in_stock
                cart[id] = quantity

            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity
        
        # Update the session cart with new quantity values
        request.session['cart'] = cart

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})
    

    def post(self, request):
        email = request.POST.get('email')
        newsletter = request.POST.get('newsletter')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        shipping_note = request.POST.get('shipping_note')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        province = request.POST.get('province')
        country = request.POST.get('country')
        save_info = request.POST.get('save_info')

        print({
            "email": email,
            "newsletter": newsletter,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "shipping_note": shipping_note,
            "city": city,
            "postal_code": postal_code,
            "province": province,
            "country": country,
            "save_info": save_info,
        })

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
