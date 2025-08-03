# 🕷️ Document Scraper & Transformer

Technologies used:

- **Scrapy**: to extract structured document metadata from the Workplace Relations site
- **MongoDB**: to store scraped metadata
- **MinIO**: to store the actual documents (PDF, DOC, HTML)
- **Dagster**: to orchestrate scraping and transformation jobs
- **FastAPI**: to transform/clean scraped documents

---

## 🧠 Overview

The pipeline performs the following tasks:

1. **Scraping**  
   Crawl workplace search results and extract ref number, date, description, and document links.  
   Save metadata to MongoDB and download the documents to MinIO.
   Data is stored in minio in this format (partition_date/ref_no.extension)

2. **document processor**  
   Triggered via FastAPI (and optionally from Dagster), this process:
   - Retrieves documents by date from MongoDB
   - Fetches and parses files from MinIO (HTML parsed using BeautifulSoup)
   - Extract the important content from the html, computes new hash and stores the result in new MinIO bucket and MongoDB collection

3. **Orchestration**  
   Dagster lets you run the scraper or transformer via UI, schedules, or programmatically.

---

## 📦 Pipelines

### 🔹 `MongoMetadataPipeline` (Scrapy Pipeline)

**Purpose**:  
- Insert metadata to MongoDB  
- Download file (PDF, DOC, or HTML)
- Store it in MinIO  
- Compute and store `file_hash`

---

### 🔹 `Document Processor (FastAPI)`

**Purpose**:  
- Given a date range:
  - Fetch documents from MongoDB
  - Clean HTML (if file is HTML)
  - Upload to new MinIO bucket (`workplace-transformed`)
  - Save enriched metadata to new collection `transformed_documents

**How to run**

docker-compose up -d 

and from the dagster ui (localhost:3000) navigate to assets and use the following conf in the launch pad of the assets:

for the spider use:
ops:
  run_spider_asset:
    config:
      start_date: "2025-01-01"
      end_date: "2025-08-01"


for the transformation process use: 
ops:
  trigger_transform_api:
    config:
      start_date: "2025-01-01"
      end_date: "2025-08-01"




