ARG TARGETPLATFORM=linux/amd64
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies:
#   libmupdf-dev  - PyMuPDF
#   build-essential, python3-dev - compile chroma-hnswlib (CrewAI -> chromadb)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmupdf-dev \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create evidence upload directory
RUN mkdir -p /tmp/whistleblower_evidence

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
