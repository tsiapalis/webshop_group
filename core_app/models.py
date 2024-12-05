from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Base class for shop items
class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Candle(Item):
    burn_time = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    CATEGORY_CHOICES = [
        ('SC', 'Scented'),
        ('PI', 'Pillar'),
        ('DE', 'Decorative'),
        ('TW', 'Twisted'),
        ('TA', 'Taper'),
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='candles/', blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = {
        "1" : "Not Great",
        "2" : "Could Be Better",
        "3" : "Good",
        "4" : "Really Good",
        "5" : "Amazing"
        }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping = models.JSONField()

    def __str__(self):
        return f"Order {self.id} belongs to {self.user.username}."

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.title} in Order {self.order.id}"

