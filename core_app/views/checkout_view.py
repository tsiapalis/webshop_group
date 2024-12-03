from django.views import View
from django.shortcuts import render, get_object_or_404
from ..models import Candle

class CheckoutView(View):
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
    