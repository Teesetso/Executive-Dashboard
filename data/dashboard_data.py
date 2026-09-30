from collections import Counter

PERIODS = ['This month', 'Last 7 days', 'Last 30 days']
STATUS_COLORS = {'Completed': '#167d6c', 'In progress': '#e8943b', 'Paused': '#d75b4c', 'Synchronized': '#8b96a7'}

def build_dashboard(period, jobs=None, error=None):
    jobs = jobs or []
    status_counts = Counter(job['status'] for job in jobs)
    type_counts = Counter(job['type'] for job in jobs)
    technician_counts = Counter(job['technician'] for job in jobs)
    paused_counts = Counter(f"{job['customer']} · {job['site']}" for job in jobs if job['status'] == 'Paused')
    overdue_jobs = [job for job in jobs if job['overdue']]
    overdue = len(overdue_jobs)
    return {
        'period': period, 'periods': PERIODS, 'jobs': jobs,
        'status_counts': status_counts, 'type_counts': type_counts,
        'technician_counts': technician_counts, 'paused_counts': paused_counts,
        'overdue_jobs': overdue_jobs, 'completed': status_counts['Completed'],
        'overdue': overdue, 'on_time': round((len(jobs) - overdue) / len(jobs) * 100) if jobs else 0,
        'status_colors': STATUS_COLORS, 'error': error,
    }
