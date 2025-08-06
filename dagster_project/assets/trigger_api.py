import requests
import os
from dagster import asset, EnvVar, MetadataValue
from utils import split_date_range_by_month

FASTAPI_TRANSFORMER_URL = os.getenv(
    "TRANSFORMER_API_URL", "http://transformer:8000")


@asset(metadata={"kedra": "rami", "description": "Trigger FastAPI transformation service."})
def trigger_transform_api(context):
    start_date = context.op_config.get("start_date")
    end_date = context.op_config.get("end_date")

    if not start_date or not end_date:
        raise ValueError("start_date and end_date must be provided in op_config")

    months = split_date_range_by_month(start_date, end_date)

    for start, end in months:
        payload = {"start_date": start, "end_date": end}
        response = requests.post(f"{FASTAPI_TRANSFORMER_URL}/transform", json=payload)

        if response.status_code == 200:
            context.log.info(f"Triggered transform API for {start} to {end}")
        else:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")

