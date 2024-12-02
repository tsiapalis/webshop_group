from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Candle

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})

        print(cart)

        items = []
        for id, quantity in cart.items():
            item = get_object_or_404(Candle, id=id)
            items.append({'item': item, 'quantity': quantity})

        print('items: ', items)
        cart_count = sum(cart.values())
        

        return render(request, 'core_app/cart.html', {'items': items, 'cart_count': cart_count})