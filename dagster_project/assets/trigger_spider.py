from dagster import asset, AssetExecutionContext, Config
import subprocess
from utils import split_date_range_by_month 

class SpiderRunConfig(Config):
    start_date: str
    end_date: str

@asset
def run_spider_asset(context: AssetExecutionContext, config: SpiderRunConfig):
    months = split_date_range_by_month(config.start_date, config.end_date)

    for start, end in months:
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
            context.log.error(f"Spider failed for {start} - {end}: {result.stderr}")
            raise RuntimeError("Spider execution failed")

        context.log.info(f"Spider finished for {start} to {end}")
        context.log.debug(result.stdout)
