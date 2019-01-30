from datetime import time


def within_business_hours(dt):
    return dt.weekday() <= 4 and time(9) <= dt.time() <= time(17)
