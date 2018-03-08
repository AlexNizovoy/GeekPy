from django.db import models

from product.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50, blank=True)

    delivery_country = models.CharField(max_length=50)
    delivery_state = models.CharField(max_length=50)
    delivery_city = models.CharField(max_length=50)
    delivery_address = models.CharField(max_length=150)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return 'Order #{}'.format(self.id)

    def total_cost(self):
        return sum(item.cost for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')

    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'Order item #{}'.format(self.id)

    def cost(self):
        return self.price * self.quantity
