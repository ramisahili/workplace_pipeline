# dagster_project/Dockerfile
FROM python:3.10-slim

WORKDIR /app/dagster_project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["dagster", "dev", "--host", "0.0.0.0", "--port", "3000"]
