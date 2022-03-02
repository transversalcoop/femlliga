from datetime import datetime, timedelta

def date_intervals(start, end):
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    if (end - start) < timedelta(days=30):
        f = lambda x: x + timedelta(days=1)
    elif (end - start) < timedelta(days=30*3):
        f = lambda x: x + timedelta(days=7)
    else:
        start = start.replace(day=1)
        f = lambda x: add_one_month(x)

    intervals = [start]
    mid = start
    while mid < end:
        mid = f(mid)
        intervals.append(mid)

    return intervals

def add_one_month(t):
    t = t.replace(day=1)
    t = t + timedelta(days=32)
    t = t.replace(day=1)
    return t
