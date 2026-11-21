from rest_framework.routers import DefaultRouter

from .views import ActualLogViewSet, PlannedBlockViewSet, TaskViewSet, WeekViewSet

router = DefaultRouter()
router.register("weeks", WeekViewSet, basename="week")
router.register("task", TaskViewSet, basename="task")
router.register("plannedblock", PlannedBlockViewSet, basename="plannedblock")
router.register("actuallog", ActualLogViewSet, basename="actuallog")

urlpatterns = router.urls

