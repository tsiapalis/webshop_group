from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Candle, Order, OrderItem, User
from django.http import HttpResponseRedirect
from django.contrib import messages

class CheckoutUtils:
    @staticmethod
    def process_cart(request):
        cart = request.session.get('cart', {})
        subTotal = 0
        items = []

        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)

            if item.in_stock == 0 or quantity > item.in_stock:
                messages.warning(
                    request,
                    f"Unfortunately, the item '{item.title}' is no longer available in the quantity you requested. "
                    f"We currently have {item.in_stock} left in stock. Please update your cart to proceed."
                )
                return None, None

            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity

class DetailsView(View):
    def get(self, request):
        cart = request.session.get('cart', {})

        items, subTotal = CheckoutUtils.process_cart(request)
        if items is None:
            return redirect('/cart')

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


        checkout = request.session.get('checkout', {})

        checkout['details'] = {
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
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ShippingView(View):
    def get(self, request):
        items, subTotal = CheckoutUtils.process_cart(request)
        if items is None:
            return redirect('/cart')

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})
    
    def post(self, request):
        contact = request.POST.get('contact')
        ship_to = request.POST.get('ship_to')
        delivery_method = request.POST.get('delivery_method')
        shipping_cost = 0

        checkout = request.session.get('checkout', {})

        checkout['shipping'] = {
            "contact": contact,
            "ship_to": ship_to,
            "delivery_method": delivery_method,
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class PaymentView(View):
    def get(self, request):
        items, subTotal = CheckoutUtils.process_cart(request)
        if items is None:
            return redirect('/cart')

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})
    
    def post(self, request):
        card_number = request.POST.get('card_number')
        holder_name = request.POST.get('holder_name')
        expiration = request.POST.get('expiration')
        cvv = request.POST.get('cvv')

        checkout = request.session.get('checkout', {})

        checkout['payment'] = {
            "card_number": card_number,
            "holder_name": holder_name,
            "expiration": expiration,
            "cvv": cvv
        }

        ''' TODO: the 'details' dict will be you used for the shipping address model we will add later.
        
        # details = request.session.get('details', {})
        
        # for key in request.POST.keys():
        #     if key != "csrfmiddlewaretoken":
        #         details[key] = request.POST.get(key)
        
        '''

        # Add to Order and OrderItem. I think its better if we move this block to payment view.
        cart = request.session.get('cart', {})

        order = Order.objects.create(user=request.user)
        for key, value in cart.items():
            candle = Candle.objects.get(id=key)
            OrderItem.objects.create(order=order, item=candle, quantity=value)


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))