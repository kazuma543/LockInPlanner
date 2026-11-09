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
        qs = Task.objects.filter(week__user=self.request.user)
        week_id = self.request.query_params.get("week")
        if week_id:
            qs = qs.filter(week_id=week_id)
        return qs

class 