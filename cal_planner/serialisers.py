from rest_framework import serializers
from .models import Week

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        field = ["id", "start_date","goal"]