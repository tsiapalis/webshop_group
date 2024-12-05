from django.views import View
from django.shortcuts import render, get_object_or_404
from ..models import Candle, Order, OrderItem, User
from django.http import HttpResponseRedirect
from django.contrib import messages

class DetailsView(View):
    def get(self, request):
        cart = request.session.get('cart', {})    

        subTotal = 0
        items = []
        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)

            if item.in_stock == 0 or quantity > item.in_stock:
                messages.success(request, "The items stock changed.")
                return HttpResponseRedirect('/cart')

            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity
        
        # Update the session cart with new quantity values
        request.session['cart'] = cart

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})
    

    def post(self, request):

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

        return render(request, 'core_app/checkout/shipping.html')

class ShippingView(View):
    def get(self, request):
        cart = request.session.get('cart', {})    
        
        subTotal = 0
        items = []
        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)

            if item.in_stock == 0 or quantity > item.in_stock:
                # TODO: return to cart provide a message in cart
                HttpResponseRedirect('/cart')

            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})
    
    def post(self, request):
        contact = request.POST.get('contact')
        ship_to = request.POST.get('ship_to')
        delivery_method = request.POST.get('delivery_method')
        shipping_cost = 0

        print({
            "contact": contact,
            "ship_to": ship_to,
            "delivery_method": delivery_method,
            "shipping_cost": shipping_cost,
        })

        checkout = request.session.get('checkout', {})

        checkout['shipping'] = {
            "contact": contact,
            "ship_to": ship_to,
            "delivery_method": delivery_method,
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class PaymentView(View):
    def get(self, request):
        cart = request.session.get('cart', {})    
        cart = request.session.get('cart', {}) 
        subTotal = 0
        items = []
        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)

            if item.in_stock == 0 or quantity > item.in_stock:
                # TODO: return to cart provide a message in cart
                HttpResponseRedirect('/cart')

            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})
    
    def post(self, request):
        card_number = request.POST.get('card_number')
        holder_name = request.POST.get('holder_name')
        expiration = request.POST.get('expiration')
        cvv = request.POST.get('cvv')

        print({
            "card_number": card_number,
            "holder_name": holder_name,
            "expiration": expiration,
            "cvv": cvv
        })

        checkout = request.session.get('checkout', {})

        checkout['payment'] = {
            "card_number": card_number,
            "holder_name": holder_name,
            "expiration": expiration,
            "cvv": cvv
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))