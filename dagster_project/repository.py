from dagster import Definitions
from assets.trigger_api import trigger_transform_api
from assets.trigger_spider import run_spider_asset

defs = Definitions(
    assets=[trigger_transform_api, run_spider_asset],
)
