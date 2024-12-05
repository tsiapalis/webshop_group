from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from ..models import Candle
from django.http import HttpResponseRedirect
from django.contrib import messages

class CartView(View):
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

        return render(request, 'core_app/cart.html', {'items': items, 'cart_count': sum(cart.values()), 'subTotal': subTotal})
    
    def post(self, request):
        method = self.request.POST.get('method', '').lower()
        item_id = self.request.POST.get('item_id', '').lower()
        if method == 'delete':
            return self.delete(request, item_id)
        
        quantity  = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        cart[item_id] = quantity

        request.session['cart'] = cart 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    def delete(self, request, item_id):
        cart = request.session.get('cart', {})
        if cart and cart[item_id]:
            cart.pop(item_id)
            request.session['cart'] = cart 

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))