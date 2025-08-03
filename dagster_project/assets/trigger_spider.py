from dagster import asset, AssetExecutionContext, Config
import subprocess

class SpiderRunConfig(Config):
    start_date: str
    end_date: str

@asset
def run_spider_asset(context: AssetExecutionContext, config: SpiderRunConfig):
    start = config.start_date
    end = config.end_date

    context.log.info(f"[SPIDER ASSET] Running spider from {start} to {end}")

    result = subprocess.run(
        [
            "scrapy", "crawl", "workplace",
            "-a", f"start_date={start}",
            "-a", f"end_date={end}"
        ],
        cwd="/app/spiders/kedra_spider",
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        context.log.error(f"Spider failed: {result.stderr}")
        raise RuntimeError("Spider execution failed")

    context.log.info("Spider finished successfully")
    context.log.debug(result.stdout)
