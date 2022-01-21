from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from core.views import TaskAPIViewSet

router = DefaultRouter()

router.register(r"tasks", TaskAPIViewSet, "tasks")

urlpatterns = [
    re_path(r"^api/v1/", include(router.urls)),
]