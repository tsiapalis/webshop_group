from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from ..models import Candle, Order, OrderItem, User
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime

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
        
        return items, subTotal

class DetailsView(View):
    def get(self, request):
        items, subTotal = CheckoutUtils.process_cart(request)
        if items is None:
            return redirect('/cart')

        return render(request, 'core_app/checkout/details.html', {'items': items, 'subTotal': subTotal})

    def post(self, request):
        allowed_keys = [
            'email', 'newsletter', 'first_name', 'last_name', 'address', 
            'shipping_note', 'city', 'postal_code', 'province', 'country', 'save_info'
        ]
        details = {key: request.POST.get(key) for key in allowed_keys}
        checkout = request.session.get('checkout', {})
        checkout['details'] = details
        request.session['checkout'] = checkout

        return HttpResponseRedirect(reverse('core_app:checkout_shipping'))

class ShippingView(View):
    def get(self, request):
        items, subTotal = CheckoutUtils.process_cart(request)
        if items is None:
            return redirect('/cart')

        checkout = request.session.get('checkout', {})
        contact = checkout['details']['email']
        ship_to = f"{checkout['details']['address']}, {checkout['details']['postal_code']}, {checkout['details']['province']}, {checkout['details']['country']}" 

        return render(request, 'core_app/checkout/shipping.html', {'items': items, 'subTotal': subTotal, 'contact': contact, 'ship_to': ship_to})
    
    def post(self, request):
        allowed_keys = ['contact', 'ship_to', 'standard_shipping']
        shipping = {key: request.POST.get(key) for key in allowed_keys}

        checkout = request.session.get('checkout', {})
        checkout['shipping'] = {
            **shipping,
            "cost": 0
        }
        request.session['checkout'] = checkout

        return HttpResponseRedirect(reverse('core_app:checkout_payment'))
    
class PaymentView(View):
    def get(self, request):
        items, subTotal = CheckoutUtils.process_cart(request)

        if items is None:
            return redirect('/cart')

        checkout = request.session.get('checkout', {})
        shipping_cost = checkout['shipping']['cost']

        total = subTotal + shipping_cost

        return render(request, 'core_app/checkout/payment.html', {'items': items, 'subTotal': subTotal, 'shipping': shipping_cost, 'total': total  })
    
    def post(self, request):
        allowed_keys = [
            'card_number', 'holder_name', 'expiration_date', 
            'cvv', 'vat_number', 'pec'
        ]

        payment_details = {key: request.POST.get(key) for key in allowed_keys}

        # check payment details
        payment_success = True

        if not payment_success:
            messages.warning(
                request,
                f"Unfortunately, the item payment failed. "
            )
            return redirect('/cart')
        

        checkout = request.session.get('checkout', {})

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
                return redirect('/cart')
            
            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity

            item.in_stock -= quantity
            item.save()
        
        checkout = request.session.get('checkout', {})

        user = {}
        if request.user.is_authenticated:
            user = request.user
        else:
            details = checkout.get('details', {})
            user = User.objects.filter(email=details.get('email')).first()

            # Create a temporary user with a random password (guest user case)
            if not user:
                user = User.objects.create_user(
                    username=details.get('email', 'guest_user'),
                    email=details.get('email', ''),
                    password=User.objects.make_random_password(),
                    first_name=details.get('first_name', ''),
                    last_name=details.get('last_name', ''),
                )

        order = Order.objects.create(
            user=user,
            created_at=datetime.now()
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                item=item['item'],
                quantity=item['quantity']
            )

        return HttpResponseRedirect(reverse('core_app:payment_confirmed', args=[order.id]))

class PaymentConfirmedView(View):
    def get(self, request, order_id=None):
        items, subTotal = CheckoutUtils.process_cart(request)

        if items is None:
            return redirect('/cart')

        checkout = request.session.get('checkout', {})
        shipping_cost = checkout['shipping']['cost']

        total = subTotal + shipping_cost
        request.session['cart'] = {}
        request.session['checkout'] = {}
        return render(request, 'core_app/checkout/payment_confirmation.html', {'items': items, 'subTotal': subTotal, 'shipping': 'Free Shipping', 'paid': total, 'order_id': order_id})
