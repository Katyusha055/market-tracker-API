# Market Tracker API

## 1) What this project is and what it does
Market Tracker API is an **educational project** (not production-ready software) that demonstrates a complete data pipeline for e-commerce platforms using RAM listings from Newegg as an example.

What the program does:
- Scrapes RAM products from Newegg.
- Normalizes product text into structured fields (brand, type, speed, capacity, etc.).
- Validates parsed data.
- Saves products and price history into PostgreSQL.
- Exposes the pipeline through a FastAPI HTTP API.

The goal is to practice API development, scraping, data normalization, validation, and SQL persistence in a single project.

---

## 2) How to install the project and dependencies

### Prerequisites
- Python 3.10+
- PostgreSQL (preferably running locally)
- **A database already created before running the API**

### Installation steps
1. Clone the repository and enter the project directory:
   ```bash
   git clone <your-repo-url>
   cd market-tracker-API
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the required PostgreSQL database (`market_tracker`):
   ```bash
   psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE market_tracker;"
   ```

5. Configure environment variables:
   - Create a `.env` file in the project root.
   - Use `program/env.example` as reference and set database credentials for `market_tracker`:
     - `DB_NAME=market_tracker`
     - `DB_USER=<your_postgres_user>`
     - `DB_PASSWORD=<your_postgres_password>`

Example `.env`:
```env
DB_NAME=market_tracker
DB_USER=postgres
DB_PASSWORD=your_password
```

> Important: the app creates tables automatically, but **does not create the database itself**.

---

## 3) How to run and start the project

Start the API server:

```bash
uvicorn api.app:app --reload
```

By default, the app runs at:
- `http://127.0.0.1:8000`

Interactive docs are generated at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 4) How to use it (endpoints)

### `GET /`
Health/status endpoint.

**Response example**
```json
{
  "status": "running",
  "service": "market-tracker"
}
```

---

### `POST /scrapper?pages=<int>`
Runs the complete scraper pipeline.

- `pages` is optional (default: `5`).
- Must be a number between 1 and 20.

**Example request**
```bash
curl -X POST "http://127.0.0.1:8000/scrapper?pages=3"
```

**Successful response shape**
```json
{
  "Products Scrapped": 0,
  "Duplicate Products": 0,
  "New Products": 0,
  "Price Data Inserted": 0
}
```

**Validation errors**
- If `pages <= 0`: HTTP 400
- If `pages > 20`: HTTP 400

---

## Notes
- The project creates tables automatically if they do not exist (`products`, `price_history`).
- It stores one row per scraping event in `price_history`, even for duplicate products.
- This codebase is designed for learning and experimentation, not for production hardening.
- For further details and explanations about the technical process and decisions taken during the development of the project itself refer to **dev_notes.md**
- For further details about the architecture of the project refer to **architecture.md**
