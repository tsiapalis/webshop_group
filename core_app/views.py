from django.shortcuts import render


def index(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'core_app/index.html', {'cart_count': cart_count})


def about(request):
    return render(request, 'core_app/about.html')

class Discovery(TemplateView):
    template_name = 'core_app/discovery.html'

    def get_context_data(self, **kwargs):
        print("Discovery view accessed!")
        selected_category = self.request.GET.get('category')

        candles = Candle.objects.filter(category=selected_category) if selected_category else Candle.objects.all()
        context = {
            'candles': candles,
            'categories': Candle.CATEGORY_CHOICES,  # Categories for the dropdown
            'selected_category': selected_category,  # Pass selected category for the dropdown
        }
        print(context)
        return context