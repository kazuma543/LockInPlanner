from datetime import timedelta

from django.db.models import DurationField, ExpressionWrapper, F, Sum

from .models import ActualLog, PlannedBlock, Task


def find_overlapping_blocks(user, start, end, exclude_id=None):
    qs = PlannedBlock.objects.filter(
        task__week__user = user,
        start_time__lt = end,
        end_time__gt = start,
    )
    if exclude_id is not None:
        qs =qs.exclude(pk=exclude_id)
    return qs

def calculate_planned_time_amount(week):
    task_summaries = PlannedBlock.objects.filter(task__week=week
                                                ).annotate(
        planned_time = ExpressionWrapper(
            F('end_time')-F('start_time'),
            output_field=DurationField()
        )
    ).values('task').annotate(
        total_planned_minutes=Sum('planned_time')
    )
    return task_summaries


def calculate_actual_time_amount(week):
    task_summaries = ActualLog.objects.filter(task__week=week
                                              ).annotate(
        actual_time = ExpressionWrapper(
            F('end_time')-F('start_time'),
            output_field=DurationField()
        )
    ).values('task').annotate(
        total_actual_minutes=Sum('actual_time')
    )
    return task_summaries

def calculate_achievement_percentage(week):
    planned_data=calculate_planned_time_amount(week)
    actual_data =calculate_actual_time_amount(week)
    
    planned_dict = {item['task']: item['total_planned_minutes'] for item in planned_data}
    actual_dict = {item['task']: item['total_actual_minutes'] for item in actual_data}
    weekly_task = Task.objects.filter(week=week).order_by('id')
    
    results = []
    for task in weekly_task:
        planned = planned_dict.get(task.id, timedelta(0))
        actual = actual_dict.get(task.id, timedelta(0))
        if planned and actual and planned.total_seconds() > 0:
            percentage = (actual.total_seconds() / planned.total_seconds()) * 100
        else:
            percentage = 0.0

        results.append({
            'task_id': task.id,
            'task_name':task.name,
            'target_minutes':task.target_minutes,
            'total_planned_minutes': planned.total_seconds()/ 60,
            'total_actual_minutes': actual.total_seconds()/ 60,
            'percentage': round(percentage, 2)  
        })

    return results