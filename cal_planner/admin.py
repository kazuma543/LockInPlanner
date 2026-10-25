from django.contrib import admin
from .models import Week, Task, PlannedBlock, ActualLog

admin.site.register(Week)
admin.site.register(Task)
admin.site.register(PlannedBlock)
admin.site.register(ActualLog)