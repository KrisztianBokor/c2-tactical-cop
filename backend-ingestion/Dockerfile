# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Hardened Runtime
FROM python:3.11-slim

# Defense hardening: run as non-root
RUN groupadd -r c2group && useradd -r -g c2group -d /app -s /sbin/nologin c2user

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . /app

USER c2user

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]