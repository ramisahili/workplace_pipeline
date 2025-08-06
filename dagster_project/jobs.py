
from dagster import define_asset_job

spider_job = define_asset_job(
    name="spider_job",
    selection=["run_spider_asset"]
)

# Job to trigger FastAPI transform only
transform_job = define_asset_job(
    name="transform_job",
    selection=["trigger_transform_api"]
)