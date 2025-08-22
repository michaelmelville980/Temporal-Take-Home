# Temporal Take-Home

Orchestrates an Order LifeCycle using Temporal's open-source SDK and dev server.

<img width="1353" height="293" alt="image" src="https://github.com/user-attachments/assets/9be53a51-4b96-4c0e-b743-b00111fa1087" />

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

I implemented three main tables (orders, payments, events) with persistence and interacted with them via (Workflow → Activity → Service → CRUD → DB).

The schema and CRUD operations felt straightforward, but I struggled with configuring engines and sessions, using the add/commit/refresh pattern, async vs. sync concepts, and later Dockerizing the database.

# Tests

I wrote unit tests for database CRUD operations and performed integration testing by running workflows against a local Temporal Server with sample CLI arguments.

All CRUD unit tests passed successfully. The order and shipping workflows completed in 10–20 seconds on average. The "Cancel order" and "Check status" signals functioned as expected, but I was unable to get the "Update address" signal working. 


## Running Tests:
```bash
poetry run pytest
```



