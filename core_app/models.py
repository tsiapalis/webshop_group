from django.db import models

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
    CATEGORY_CHOICES = [
        ('SC', 'Scented'),
        ('US', 'Unscented'),
        ('DE', 'Decrotive'),
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='candles/', blank=True, null=True)

    def __str__(self):
        return self.title