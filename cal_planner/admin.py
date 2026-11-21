from django.contrib import admin

from .models import ActualLog, PlannedBlock, Task, Week

admin.site.register(Week)
admin.site.register(Task)
admin.site.register(PlannedBlock)
admin.site.register(ActualLog)