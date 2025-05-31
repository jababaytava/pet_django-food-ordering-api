from rest_framework import serializers
from orders.models import Order, OrderItem
from orders.tasks import confirm_order_task
from tables.models import Table


class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "dish", "dish_name", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())

    class Meta:
        model = Order
        fields = ["id", "status", "created_at", "table", "items"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        table = validated_data.pop("table")
        user = self.context["request"].user

        order = Order.objects.create(user=user, table=table)

        for item_data in items_data:
            dish = item_data["dish"]
            if not dish.is_available:
                raise serializers.ValidationError(
                    {"items": [f"Dish '{dish.name}' is not available."]}
                )

            OrderItem.objects.create(order=order, **item_data)

        confirm_order_task.delay(order.id)
        return order
