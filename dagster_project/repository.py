from dagster import Definitions
from assets.trigger_api import trigger_transform_api
from assets.trigger_spider import run_spider_asset
from jobs import spider_job, transform_job
from schedules import spider_schedule, transform_schedule

defs = Definitions(
    assets=[trigger_transform_api, run_spider_asset],
    jobs=[spider_job, transform_job],
    schedules=[spider_schedule, transform_schedule],
)
