from django.shortcuts import render
from rest_framework import viewsets
from .models import Week
from .serialisers import WeekSerializer
# Create your views here.

class WeekViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeekSerializer

    def get_queryset(self):
        return Week.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)