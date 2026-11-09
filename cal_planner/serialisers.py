from rest_framework import serializers
from .models import Week, Task, PlannedBlock

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ["id", "start_date","goal"]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "week", "name","target_minutes"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            fields["week"].queryset = Week.objects.filter(user=request.user)
        return fields

class PlannedBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedBlock
        fields = ["id", "task", "start_time", "end_time"]
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            fields["task"].queryset = Task.objects.filter(week__user=request.user)
        return fields
    
