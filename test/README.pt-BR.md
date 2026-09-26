# 🧪 Suíte de Testes e Garantia de Qualidade (QA) - NuClone Core API
[![Leia em Inglês](https://img.shields.io/badge/Language-English_🇺🇸-blue.svg)](README.md)

Este módulo reúne a arquitetura de testes automatizados da aplicação, projetada para garantir alta resiliência, integridade transacional e segurança em operações financeiras e de autenticação.

---

## 📊 Métrica Atual de Cobertura de Código

A suíte de testes atinge **92% de cobertura global de código** (`Code Coverage`), com **100% de cobertura nos componentes críticos de segurança e persistência de dados**.

| Módulo / Camada | Cobertura | Status |
| :--- | :---: | :--- |
| **`src/core/security.py`** | **100%** | 🛡️ Autenticação & tokens JWT totalmente validados |
| **`src/modules/auth/`** | **100%** | 🔐 Repositório e Router de Login integrados |
| **`src/modules/ledger/`** | **100%** | 💳 Extrato, lançamentos e agregações de saldo |
| **`src/modules/account/repository.py`** | **100%** | 🏦 Inicialização e tratamento de saldo zerado |
| **`src/modules/customer/`** | **98%** | 👤 Operações de clientes e regras de negócio |
| **Média Geral do Projeto** | **92%** | 🎯 Alta confiabilidade para ambiente de produção |

---

## 🏗️ Estrutura da Arquitetura de Testes

A suíte utiliza **Pytest** e é organizada em três camadas estratégicas de isolamento:

| test/  

├── e2e/          Testes de ponta a ponta em endpoints da API (FastAPI TestClient)

├── integration/   Testes de integração com banco de dados (Sessões SQLAlchemy)

└── unit/           Testes unitários isolados com Mocks (Regras de negócio e Segurança)



## 🚀 Entregas e Escopo Testado

- [x] **Segurança e Autenticação (`src/core/security.py` & `src/modules/auth/`)**:
  - Validação de criptografia de senhas via Passlib/Bcrypt.
  - Geração e validação de tokens JWT (`access_token`) com expiração estática e dinâmica.
  - Validação de erros HTTP 401 para credenciais inválidas e headers malformatados no `OAuth2PasswordRequestForm`.

- [x] **Livro Razão e Extrato (`src/modules/ledger/`)**:
  - Testes de integridade em buscas de transações e filtros por data/fuso horário.
  - Cálculo acumulado de movimentações financeiras na janela diurna e noturna (`get_total_gasto_janela`).

- [x] **Gestão de Limites (`src/modules/limits/`)**:
  - Validação de trava transacional por extrapolação de limite (`ExceededLimitException`).
  - Testes de regras de horário para limite diurno e noturno.

- [x] **Contas e Inicialização Dinâmica (`src/modules/account/`)**:
  - Fallback de integridade com criação automática de saldo zerado (`0.00`) para novas contas.

---

## 📌 Próximos Passos & Melhorias

- [ ] Elevar a cobertura do módulo `src/modules/pix/service.py` para 95%+.
- [x] Implementar execução contínua via pipeline de CI/CD com GitHub Actions.

---

## 🛠️ Como Executar os Testes Localmente

### Executar a suíte de testes
```bash
pytest --cov=src --cov-report=html