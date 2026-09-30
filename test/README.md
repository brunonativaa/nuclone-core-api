# 🧪 Testing and Quality Assurance (QA) Suite - NuClone Core API
[![Read in Portuguese](https://img.shields.io/badge/Language-Portugu%C3%AAs_🇧🇷-blue.svg)](README.pt-BR.md)

This module brings together the application’s automated testing architecture, designed to ensure high resilience, transactional integrity, and security in financial and authentication operations.

---

## 📊 Current Code Coverage Metrics

The test suite achieves **92% overall code coverage** (`Code Coverage`), with **100% coverage of critical security and data persistence components**.

| Module / Layer | Coverage | Status |
| :--- | :---: | :--- |
| **`src/core/security.py`** | **100%** | 🛡️ Authentication & fully validated JWT tokens |
| **`src/modules/auth/`** | **100%** | 🔐 Integrated repository and login router |
| **`src/modules/ledger/`** | **100%** | 💳 Statements, transactions, and balance aggregations |
| **`src/modules/account/repository.py`** | **100%** | 🏦 Initialization and handling of zero balances |
| **`src/modules/customer/`** | **98%** | 👤 Customer operations and business rules |
| **Overall Project Average** | **92%** | 🎯 High reliability for production environment |

---

## 🏗️ Test Architecture Structure

The suite uses **Pytest** and is organized into three strategic layers of isolation:

| test/

├── e2e/          End-to-end tests on API endpoints (FastAPI TestClient)

├── integration/   Database integration tests (SQLAlchemy sessions)

└── unit/           Isolated unit tests with mocks (business rules and security)



## 🚀 Deliverables and Tested Scope

- [x] **Security and Authentication (`src/core/security.py` & `src/modules/auth/`)**:
  - Password encryption validation via Passlib/Bcrypt.
  - Generation and validation of JWT tokens (`access_token`) with static and dynamic expiration.
  - Validation of HTTP 401 errors for invalid credentials and malformed headers in `OAuth2PasswordRequestForm`.

- [x] **General Ledger and Statement (`src/modules/ledger/`)**:
  - Integrity tests for transaction searches and filters by date/time zone.
  - Cumulative calculation of financial transactions during the day and night windows (`get_total_gasto_janela`).

- [x] **Limit Management (`src/modules/limits/`)**:
  - Validation of transaction locks due to limit exceedance (`ExceededLimitException`).
  - Testing of time-based rules for day and night limits.

- [x] **Accounts and Dynamic Initialization (`src/modules/account/`)**:
  - Integrity fallback with automatic creation of a zero balance (`0.00`) for new accounts.

---

## 📌 Next Steps & Improvements

- [ ] Increase coverage of the `src/modules/pix/service.py` module to 95%+.
- [x] Implement continuous execution via a CI/CD pipeline with GitHub Actions.

---

## 🛠️ How to Run Tests Locally

### Run the test suite
```bash
pytest --cov=src --cov-report=html