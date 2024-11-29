from django.shortcuts import render


def index(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'core_app/index.html', {'cart_count': cart_count})


def about(request):
    return render(request, 'core_app/about.html')