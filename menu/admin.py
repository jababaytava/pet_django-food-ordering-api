from django.contrib import admin
from menu.models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available")
    search_fields = ("name",)
