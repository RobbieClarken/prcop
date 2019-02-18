from datetime import datetime, time, timedelta


START_OF_DAY = time(9)
END_OF_DAY = time(17)
SAT = 5
SUN = 6


def within_business_hours(dt):
    return dt.weekday() < SAT and START_OF_DAY <= dt.time() <= END_OF_DAY


def business_hours_between_dates(start, end):

    if start.time() < START_OF_DAY:
        start = datetime.combine(start.date(), START_OF_DAY)
    elif start.time() >= END_OF_DAY:
        start = datetime.combine(start.date() + timedelta(days=1), START_OF_DAY)

    if start.weekday() in (SAT, SUN):
        start = datetime.combine(start + timedelta(days=start.weekday() - 4), START_OF_DAY)

    if end.time() <= START_OF_DAY:
        end = datetime.combine(end.date() - timedelta(days=1), END_OF_DAY)
    elif end.time() > END_OF_DAY:
        end = datetime.combine(end.date(), END_OF_DAY)

    if end.weekday() in (SAT, SUN):
        end = datetime.combine(end - timedelta(days=end.weekday() - 4), END_OF_DAY)

    if end <= start:
        return timedelta(0)

    outside_business_hours = 0
    d = start.date()
    while d < end.date():
        outside_business_hours += 24 if d.weekday() in (SAT, SUN) else 24 - 17 + 9
        d += timedelta(days=1)

    return end - start - timedelta(hours=outside_business_hours)
