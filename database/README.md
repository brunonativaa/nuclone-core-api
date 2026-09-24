# 📐 Nuclone - Core Banking & Pix Ledger API

[![Read in Portuguese](https://img.shields.io/badge/Language-Portugu%C3%AAs_🇧🇷-blue.svg)](README.pt-BR.md)
[![Python Version](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)

Nuclone is a high-performance Core Banking & Pix API built with Python 3.12 and FastAPI. It simulates enterprise banking infrastructure through double-entry ledger operations, transactional concurrency safety, dynamic daily/nightly operational limits, and JWT-based multi-tenant authentication.

---

### 🏗️ Architectural Decisions & Domain Modeling

The system is designed as a **Modular Monolith (Package by Feature)**, organizing source code strictly by business domains (`modules/customer`, `modules/account`, `modules/pix`, `modules/ledger`). This design pattern drastically reduces cognitive load, minimizes coupling, and provides a clear migration path toward microservices if required.

#### Key Engineering Highlights:
- **Volatile State Isolation (3NF):** The `account_balance` entity is separated into a 1:1 relationship with `account`. This isolates high-frequency write operations (balance updates) from static master data, mitigating database lock contention.
- **Multi-Account Flexibility (1:N):** Supports scalable 1:N relations between `customer` and `account`, allowing a single customer to hold multiple active accounts. The same strategy applies to `phone` and `address` models.
- **Financial Flow Traceability:** The `transaction` ledger tracks operations at the granular account level via direct foreign keys (`source_account_id` and `destination_account_id`), ensuring accurate auditability across account boundaries.
- **Concurrency Control & Safety:** Implements pessimistic locking (`SELECT FOR UPDATE`) during Pix transfers to prevent race conditions and balance inconsistencies in concurrent execution threads.
- **Double-Entry Ledger System:** All monetary movements are logged as immutable debit and credit ledger events, guaranteeing full compliance for account statement generation.
- **Dynamic Operational Limits:** Enforces BACEN-aligned day/night transaction thresholds per customer account.
- **Stateless Authentication (IAM):** OAuth2 with JWT handles user identity context, securing endpoint routes and enforcing strict account-level data isolation.

---

## 🛠️ Tech Stack

- **Core:** Python 3.12, FastAPI
- **Data & Persistence:** SQLAlchemy 2.0 (ORM), PostgreSQL, SQLite (`:memory:` for testing)
- **Validation & Serialization:** Pydantic v2
- **Testing & Quality Assurance:** Pytest, Pytest-Cov, HTTPX
- **Containerization & Dev Tools:** Docker, Docker Compose, Postman

---

## 📊 Database & Domain Architecture Diagram

<i>image of the diacram</i>
![Nuclone Diagram](docs/Nuclone-Core.png)



```mermaid
graph TD
    Client[Client / Postman] -->|1. OAuth2 Bearer Token| Router[FastAPI Domain Routers]
    Router -->|2. Validate Identity| AuthGuard[Auth Middleware / Security]
    Router -->|3. Check Operating Thresholds| LimitService[Operational Limits Service]
    LimitService -->|4. Validate Rules| LimitDB[(Limits Table)]
    Router -->|5. Execute Transfer with Lock| PixService[Pix Engine / Core Banking]
    PixService -->|6. Double-Entry Posting| LedgerDB[(Immutable Ledger)]

