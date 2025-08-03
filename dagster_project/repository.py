from dagster import Definitions
from jobs import spider_job
from assets.trigger_api import trigger_transform_api
from assets.trigger_spider import run_spider_asset

defs = Definitions(
    # jobs=[spider_job],
    assets=[trigger_transform_api, run_spider_asset],
)
