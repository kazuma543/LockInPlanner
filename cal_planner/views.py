from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Week, Task, PlannedBlock, ActualLog
from .serialisers import WeekSerializer, TaskSerializer, PlannedBlockSerializer, ActualLogSerializer
from .services import calculate_achievement_percentage


# Create your views here.

class WeekViewSet(viewsets.ModelViewSet):
    serializer_class = WeekSerializer

    def get_queryset(self):
        return Week.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=True, methods=['get'], url_path='achievement-percentages')
    def get_achievement_percentage(self, request, pk=None):
        
        week = self.get_object()
        
    
        data = calculate_achievement_percentage(week=week)
        return Response(data)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.filter(week__user=self.request.user)
        week_id = self.request.query_params.get("week")
        if week_id:
            qs = qs.filter(week_id=week_id)
        return qs

class PlannedBlockViewSet(viewsets.ModelViewSet):
    serializer_class = PlannedBlockSerializer

    def get_queryset(self):
        qs = PlannedBlock.objects.filter(task__week__user=self.request.user)
        task_id = self.request.query_params.get("task")
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs
    
class ActualLogViewSet(viewsets.ModelViewSet):
    serializer_class = ActualLogSerializer

    def get_queryset(self):
        qs = ActualLog.objects.filter(task__week__user=self.request.user)
        task_id = self.request.query_params.get("task")
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs
    
