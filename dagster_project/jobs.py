from dagster import job, op, In, String, ConfigurableResource

@op(
    config_schema={
        "start_date": String,
        "end_date": String,
    }
)
def run_spider(context):
    import subprocess

    start = context.op_config["start_date"]
    end = context.op_config["end_date"]

    context.log.info(f"Running spider from {start} to {end}")

    subprocess.run(
        [
            "scrapy", "crawl", "workplace",
            "-a", f"start_date={start}",
            "-a", f"end_date={end}"
        ],
        cwd="/app/spiders/kedra_spider"
    )

@job
def spider_job():
    run_spider()
