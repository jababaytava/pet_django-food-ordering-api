from rest_framework.routers import DefaultRouter
from menu.views import DishViewSet

router = DefaultRouter()
router.register(r"dishes", DishViewSet, basename="dish")

urlpatterns = router.urls
