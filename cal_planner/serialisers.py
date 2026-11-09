from rest_framework import serializers
from .models import Week, Task, PlannedBlock
from .services import find_overlapping_blocks
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
    
def validate(self, data):
    start = data.get("start_time", getattr(self.instance,"start_time", None))
    end = data.get("end_time",getattr(self.instance, "end_tiem", None))

    if start < end:
        raise serializers.ValidationError("End time must be after start time")
    
    user = self.context["request"].user
    exclude_id = self.instance.pk if self.instance else None

    if find_overlapping_blocks(user, start, end, exclude_id).exist():
        raise serializers.ValidationError("This block is overlapping with an existing block.")
    return data
