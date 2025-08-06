from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def split_date_range_by_month(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    current = start_date.replace(day=1)
    months = []

    while current <= end_date:
        month_start = current
        month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)
        if month_end > end_date:
            month_end = end_date
        months.append((month_start.strftime("%Y-%m-%d"),
                      month_end.strftime("%Y-%m-%d")))
        current = month_start + relativedelta(months=1)

    return months
