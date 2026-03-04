# Architecture

This project follows a simple, linear architecture with four layers. The program flow is **only** the following:

1. Web Scrapper
2. Normalization Layer
3. Persistence Layer
4. API Layer

```text
[1) Web Scrapper]
        |
        v
[2) Normalization Layer]
        |
        v
[3) Persistence Layer]
        |
        v
[4) API Layer]
```

## 1) Web Scrapper
Responsible for fetching raw product data from external web pages.

**Files in this layer:**
- `program/scrapper/web_scrapper.py`

## 2) Normalization Layer
Responsible for cleaning, parsing, validating, and adapting scraped data into a structured format suitable for storage.

**Files in this layer:**
- `program/normalizers/normalizer.py`
- `program/normalizers/validator.py`
- `program/normalizers/sql_utils.py`

## 3) Persistence Layer
Responsible for database connection, schema initialization, and insert/update operations.

**Files in this layer:**
- `program/db_utils/connect.py`
- `program/db_utils/schema.py`
- `program/db_utils/writer.py`

## 4) API Layer
Responsible for exposing HTTP endpoints and triggering the full pipeline.

**Files in this layer:**
- `api/app.py`
- `program/scrapper_service.py`
