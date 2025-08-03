FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY kedra_spider/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY kedra_spider /app/kedra_spider

# Copy scrapy.cfg from current context
COPY scrapy.cfg /app/scrapy.cfg

WORKDIR /app/kedra_spider

ENTRYPOINT ["scrapy"]
CMD ["crawl", "workplace"]
