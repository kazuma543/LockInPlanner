from rest_framework.routers import DefaultRouter
from .views import WeekViewSet

router = DefaultRouter()
router.register("weeks", WeekViewSet, basename="week")

urlpatterns = router.urls

