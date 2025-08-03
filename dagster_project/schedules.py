from dagster import schedule
from jobs import spider_job

@schedule(cron_schedule="0 6 * * *", job=spider_job, execution_timezone="UTC")
def daily_spider_schedule(_context):
    return {}
