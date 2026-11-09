from .models import PlannedBlock

def find_overlapping_blocks(user, start, end, exclude_id=None):
    qs = PlannedBlock.objects.filter(
        task_week_user = user,
        start_time_lt = end,
        end_time_gt = start,
    )
    if exclude_id is not None:
        qs =qs.exclude(pk=exclude_id)
    return qs