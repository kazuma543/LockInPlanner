from rest_framework.routers import DefaultRouter
from .views import WeekViewSet, TaskViewSet

router = DefaultRouter()
router.register("weeks", WeekViewSet, basename="week")
router.register("task", TaskViewSet, basename="task")
urlpatterns = router.urls

