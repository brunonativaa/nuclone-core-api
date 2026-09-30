# 🚀 Nuclone Core API

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Poetry](https://img.shields.io/badge/Poetry-2.0-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)](https://python-poetry.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

> **High-throughput Core Banking Engine** simulating critical financial operations — including customer onboarding, ledger account management, dynamic PIX payment processing, and transaction safety with 95% test coverage.

---

## 🏛️ Financial System Domain Overview

The **Nuclone Core API** acts as an enterprise-grade backend infrastructure designed to emulate real-world fintech banking systems. Built on top of **ACID-compliant relational models**, the engine guarantees data integrity, concurrency safety, and strict business rule enforcement across core financial domains:

                             │    Nuclone Core API    │
                             └───────────┬────────────┘
                                         │
        ┌──────────────────┬─────────────┼─────────────┬──────────────────┐
        ▼                  ▼             ▼             ▼                  ▼
    ┌─────────┐       ┌───────────┐  ┌──────────┐  ┌───────────┐     ┌───────────┐
    │ Customer│       │  Account  │  │   Auth   │  │  Ledger   |     │   PIX     | │                                               
    │ Onboard │       │ Management│  │  & JWT   │  │ & Balance │     │ Transfers │
    └─────────┘       └───────────┘  └──────────┘  └───────────┘     └───────────┘


### 🧠 Core Banking Modules & Business Capabilities

1. **Customer Onboarding & Identity (`/customer`)**
   - Strictly sanitizes and validates Pydantic schemas for national tax IDs (CPF), full profiles, and legal compliance.
2. **Account Management & Limits (`/account`, `/limits`)**
   - Handles multi-type account creation, dynamic PIX limits control, time-window transaction restriction, and status lifecycle management.
3. **Authentication & Security (`/auth`)**
   - Enforces stateless OAuth2 / JWT authentication using dynamic cryptographic signatures (`python-jose[cryptography]` & `passlib`).
4. **Transactional Ledger (`/ledger`)**
   - Implements immutable transaction records, real-time balance calculations, audit logs, and double-entry accounting safety.
5. **PIX Instant Payments Engine (`/pix`)**
   - Manages PIX keys (CPF, Email, Random UUID) and executes instantaneous peer-to-peer balance transfers with concurrency validation.

---

---

## 📊 Performance & Quality Assurance

The system is tested under rigorous quality engineering standards to guarantee performance under high concurrency loads:

- **Unit & Integration Suite:** **69 passed tests (100% success rate)** with **95% overall code coverage**.
- **Load & Stress Testing (Locust):** Tested under 50 simultaneous virtual users executing concurrent transactions, achieving zero deadlocks and 0.0% error rate across 2,700+ consecutive requests (~20 req/s).

---

## 📁 Detailed Module Documentation

For deep technical specifications, data models, and module-specific configurations, please refer to the dedicated sub-docs:

| Sub-Documentation | Domain Description | Language |
| :--- | :--- | :--- |
| 🗄️️ [Database Architecture](database/README.md) | PostgreSQL schemas, SQLAlchemy ORM mappings & Alembic migrations. | Portuguese |
| 🧪 [Testing & Coverage](test/README.md) | Pytest suite, mock strategies, coverage reporting, and Locust load tests. | Portuguese |

---   