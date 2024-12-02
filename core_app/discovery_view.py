from django.views import View
from .models import Candle
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q

class Discovery(View):
    def get(self, request, item_id=None):
        if item_id:
            item = get_object_or_404(Candle, id=item_id)
            return render(request, 'core_app/discovery/detailed_item.html', {'item': item})
        else:
            cart = request.session.get('cart', {})
            cart_count = sum(cart.values())
            items = Candle.objects.all()
            return render(request, 'core_app/discovery/discovery.html', {'cart_count': cart_count, 'items': items})

    def post(self, request): 
        product_id  = request.POST.get('product')
        quantity_to_add  = int(request.POST.get('quantity'))

        cart = request.session.get('cart') 
        if cart: 
            quantity = cart.get(product_id) 
            if quantity: 
                cart[product_id] = quantity+quantity_to_add
            else: 
                cart[product_id] = quantity_to_add
        else: 
            cart = {} 
            cart[product_id] = quantity_to_add

        request.session['cart'] = cart 
        print('cart', request.session['cart']) 

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class SearchView(View):
    def get(self, request):
        search_query = request.GET.get('q', '')  
        if search_query:
            items = Candle.objects.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )
        else:
            items = Candle.objects.all()  

        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())

        categories = Candle.CATEGORY_CHOICES

        return render(request, 'core_app/discovery/discovery.html', {
            'cart_count': cart_count,
            'items': items,
            'categories': categories,
            'search_query': search_query,  
        })