from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.homeworks import views


router = DefaultRouter()
router.register(r"homeworks", views.HomeworkViewSet, basename="homeworks")

homework_tasks_router = NestedDefaultRouter(router, r"homeworks", lookup="homework")
homework_tasks_router.register(
    r"tasks",
    views.HomeworkTaskViewSet,
    basename="homework-tasks",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(homework_tasks_router.urls)),
]
