from django.shortcuts import render

from rest_framework import generics, views, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Task
from core.serializers import TaskListSerializer, TaskDetailsSerializer, TaskUpdateSerializer
# Create your views here.


class TaskAPIViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            serializer_class = TaskListSerializer
        elif self.action == "update":
            serializer_class = TaskUpdateSerializer
        else:
            serializer_class = TaskDetailsSerializer

        return serializer_class

    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if task.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)
