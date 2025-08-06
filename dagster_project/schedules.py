from dagster import ScheduleDefinition
from jobs import spider_job, transform_job
from datetime import datetime, timedelta


def dynamic_month_dates():
    today = datetime.today()
    start = today.replace(day=1)
    end = (start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def spider_run_config():
    start_date, end_date = dynamic_month_dates()
    return {
        "ops": {
            "run_spider_asset": {
                "config": {
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
        }
    }


spider_schedule = ScheduleDefinition(
    job=spider_job,
    cron_schedule="*/2 * * * *",
    run_config_fn=spider_run_config,
    name="spider_every_10min"
)


def transform_run_config():
    start_date, end_date = dynamic_month_dates()
    return {
        "ops": {
            "trigger_transform_api": {
                "config": {
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
        }
    }


transform_schedule = ScheduleDefinition(
    job=transform_job,
    cron_schedule="*/2 * * * *",
    run_config_fn=transform_run_config,
    name="transform_every_30min"
)
