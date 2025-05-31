from rest_framework import generics, permissions
from orders.serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
import os


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class TelegramUpdateOrderStatusView(APIView):
    def post(self, request):
        print(request.data)
        secret = request.data.get("secret")
        if secret != os.getenv("TELEGRAM_SECRET"):
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        order_id = request.data.get("order_id")
        new_status = request.data.get("status")

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return Response({"success": True})
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
