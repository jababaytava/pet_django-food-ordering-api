from rest_framework import viewsets, permissions, mixins
from menu.models import Dish
from menu.serializers import DishSerializer


class DishViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.AllowAny]
