from django.views import View
from .models import Candle
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q

class Discovery(View):
    def get(self, request, item_id=None): # item_id=None,  category=None
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())
    
        if item_id:
            item = get_object_or_404(Candle, id=item_id)
            print(cart)
            print(item_id)
            quantity = cart.get(str(item_id))
            print("quantity: ", quantity)
            return render(request, 'core_app/discovery/detailed_item.html', {'cart_count': cart_count, 'item': item, 'quantity': quantity})
        else:
            category = request.GET.get('category', None)
            search_query = request.GET.get('search',None)

        items = []
        if category and search_query:
            items = Candle.objects.filter(
                Q(category=category) & (Q(title__icontains=search_query) | Q(description__icontains=search_query))
            )
        elif category:
            items = Candle.objects.filter(category=category)
        elif search_query:
            items = Candle.objects.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        else:
            items = Candle.objects.all()
        
        return render(request, 'core_app/discovery/discovery.html', {'cart_count': cart_count, 'items': items})


    def post(self, request): 
        item_id  = request.POST.get('product')
        new_quantity  = int(request.POST.get('quantity'))

        if not item_id or new_quantity < 0:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart = request.session.get('cart', {})

        if new_quantity == 0:
            cart.pop(item_id, None)
        else:
            cart[item_id] = new_quantity

        request.session['cart'] = cart 

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
