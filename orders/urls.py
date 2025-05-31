from django.urls import path
from orders.views import (
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    TelegramUpdateOrderStatusView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path(
        "update-status/",
        TelegramUpdateOrderStatusView.as_view(),
        name="telegram-order-update",
    ),
]
