from .models import PlannedBlock, ActualLog
from django.db.models import F, Sum, ExpressionWrapper, DurationField
from collections import defaultdict

def find_overlapping_blocks(user, start, end, exclude_id=None):
    qs = PlannedBlock.objects.filter(
        task_week_user = user,
        start_time_lt = end,
        end_time_gt = start,
    )
    if exclude_id is not None:
        qs =qs.exclude(pk=exclude_id)
    return qs

def calculate_plannned_time_amout(self):
    task_summaries = PlannedBlock.objects.annotate(
        planned_time = ExpressionWrapper(
            F('end_time')-F('start_time'),
            output_field=DurationField()
        )
    ).values('task').annotate(
        total_planned_time=Sum('planned_time')
    )
    return task_summaries


def calculate_actual_time_amout(self):
    task_summaries = ActualLog.objects.annotate(
        actual_time = ExpressionWrapper(
            F('end_time')-F('start_time'),
            output_field=DurationField()
        )
    ).values('task').annotate(
        total_actual_time=Sum('actual_time')
    )
    return task_summaries

def calculate_achievement_percentage(self):
    planned_data=self.calculate_planned_time_amount()
    actual_data = self.calculate_actual_time_amout()

    merged_tasks = defaultdict(lambda: {'planned': None, 'actual': None})
    for item in planned_data:
        task_id = item['task']
        merged_tasks[task_id]['planned'] = item['total_planned_time']
    
    for item in actual_data:
        task_id = item['task']
        merged_tasks[task_id]['actual'] = item['total_actual_time']

    results = []
    for task_id, times in merged_tasks.items():
        planned = times['planned']
        actual = times['actual']
        if planned and actual and planned.total_seconds() > 0:
            percentage = (actual.total_seconds() / planned.total_seconds()) * 100
        else:
            percentage = 0.0 

        results.append({
            'task_id': task_id,
            'total_planned_time': planned,
            'total_actual_time': actual,
            'percentage': round(percentage, 2)  
        })

    return results