from django.shortcuts import render
from rest_framework import viewsets
from .models import Week, Task
from .serialisers import WeekSerializer, TaskSerializer
# Create your views here.

class WeekViewSet(viewsets.ModelViewSet):
    serializer_class = WeekSerializer

    def get_queryset(self):
        return Week.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)