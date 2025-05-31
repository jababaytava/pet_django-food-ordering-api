from django.db import models
from django.conf import settings
from menu.models import Dish
from tables.models import Table


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Очікує підтвердження"),
        ("confirmed", "Підтверджено"),
        ("canceled", "Скасовано"),
        ("completed", "Виконано"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)

    def __str__(self):
        return f"Order #{self.pk} ({self.user.email})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"
