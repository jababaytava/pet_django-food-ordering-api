from rest_framework import serializers
from orders.models import Order, OrderItem
from orders.tasks import confirm_order_task


class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "dish", "dish_name", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "items"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        order = Order.objects.create(user=user)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        confirm_order_task.delay(order.id)
        return order
