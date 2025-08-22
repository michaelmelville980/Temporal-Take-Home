# Temporal Take-Home

Orchestrates an Order LifeCycle using Temporal's open-source SDK and dev server.

# Quick Start

**0) Install deps**
```bash
brew install temporal
poetry install
```

**1) Start Temporal (dev)** 
```bash
temporal server start-dev
```

**2) Start Postgres (Docker)**
```bash
docker compose up -d app-db
```

**3) Configure env**
Create `.env` in the project root:

```env
# .env
DATABASE_URL=postgresql://temporal:temporal@localhost:5434/mydb
TEMPORAL_HOST=localhost:7233
```

**4) Apply DB migrations**
```bash
PYTHONPATH=./src poetry run alembic upgrade head
```

**5) Run workers (two terminals)**
```bash
PYTHONPATH=./src poetry run python -m workers.order_worker
PYTHONPATH=./src poetry run python -m workers.shipping_worker
```

**6) Start a workflow (new terminal)**
```bash
PYTHONPATH=./src poetry run python src/cli.py start abc-001 123   --items '[{"name":"apple","qty":1,"price":5.00}]'   --address '{"address":"575 Lake Dr.","city":"Columbus","state":"OH","zipcode":"43210"}'
```

**7) Watch it in the UI**
http://localhost:8233

# Signals & Queries

**Update address**
```bash
PYTHONPATH=./src poetry run python src/cli.py update-address abc-001   --address '{"address":"5 Lake Dr.","city":"Temp","state":"AL","zipcode":"43561"}'
```

**Cancel order**
```bash
PYTHONPATH=./src poetry run python src/cli.py cancel abc-001
```

**Check status**
```bash
PYTHONPATH=./src poetry run python src/cli.py status abc-001
```

# Schema & Migrations

I set up a local Postgres database, created a role, and stored credentials in a git-ignored .env. While I’ve used Postgres with Prisma (JS ORM), this was my first time with Python tools, so I chose SQLAlchemy (schema/ORM) and Alembic (migrations).

I implemented three main tables (orders, payments, events), made small tweaks, and wrote tests for Orders and Payments. With more time, I’d also test event logging and refactor some redundant session/commit code.

For idempotency, I added checks to see if records already exist and validated state before updating. I also wrote tests specific to this behavior.

The schema and CRUD operations felt straightforward, but I struggled with configuring engines and sessions, using the add/commit/refresh pattern, async vs. sync concepts, and later Dockerizing the database.


# Tests

I wrote tests for database CRUD operations but not for Temporal. Instead, I validated parts of OrderWorkflow in the UI with sample CLI arguments. I was unable to resolve a bug where OrderEvents continually called ShippingEvents and didn't check signals. 

## Running Tests:
```bash
poetry run pytest
```



