from django.contrib import admin
from .models import Candle, Review, Order, OrderItem

# Register your models here.
admin.site.register(Candle)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)