from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Candle
from django.http import HttpResponseRedirect

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})

        subTotal = 0
        items = []
        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)
            items.append({'item': item, 'quantity': quantity})
            subTotal += item.price * quantity

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
            print("in here")
            cart.pop(item_id)
            request.session['cart'] = cart 

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))