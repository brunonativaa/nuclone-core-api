🚀 Nuclone Core API<br>
O Nuclone Core API é uma engine de serviços bancários (Core Banking API) desenvolvida em Python e FastAPI. O sistema simula operações financeiras críticas de alta concorrência — incluindo onboarding de clientes, gestão de contas e processamento transacional de pagamentos PIX —, garantindo consistência relacional, isolamento de dados e resiliência sob carga.

📌 Principais Funcionalidades

Gerenciamento de Clientes & Contas: Onboarding com sanitização e validação estrita de schemas Pydantic (CPF, dados pessoais e regras de negócio).

Módulo PIX Transacional: Registro de chaves (E-mail, CPF, Aleatória) e execução de transferências com validação de saldo e concorrência.

Resiliência e Persistência: Mapeamento ORM com SQLAlchemy e PostgreSQL rodando sob infraestrutura isolada em containers Docker com volumes persistentes.

Pipeline de Qualidade (QA): Suíte completa de testes unitários mockados, testes de integração e testes de carga simulando estresse de usuários simultâneos.<br>

-----------------------

🛠️ Arquitetura e Tecnologias


                +-----------------------------------+
                  |          Locust / Clients         |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |         FastAPI / Uvicorn         |
                  |     (Routers / Schemas Pydantic)  |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |      Service Layer (Domain)       |
                  |  (Business Rules & Exceptions)    |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |      SQLAlchemy ORM Layer         |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------+-----------------+
                  |     PostgreSQL (Docker Volume)    |
                  +-----------------------------------+

-------------------

Framework: FastAPI / Uvicorn

Linguagem & Gerenciador: Python 3.11+ / Poetry

Banco de Dados: PostgreSQL

ORM: SQLAlchemy

Testes Unitários & Cobertura: Pytest, pytest-cov, unittest.mock

Testes de Performance: Locust

Containerização: Docker & Docker Compose

-------------------------

🧪 Qualidade de Código & Testes
A API foi projetada sob diretrizes rigorosas de testabilidade, separando a camada de apresentação das regras de domínio.

1. Cobertura de Testes Unitários (pytest-cov)
Toda a camada de controle/rotas e serviços possui 100% de cobertura de código, incluindo cenários de caminho feliz e tratamento resiliente de exceções (404 Not Found, 400 Bad Request, 422 Unprocessable Content).

---

2. Testes de Carga e Estresse (Locust)
A API foi submetida a testes de performance simulando múltiplas jornadas em paralelo (geração dinâmica de CPFs/e-mails, consultas de saldo e transferências de alta concorrência).

Usuários Simultâneos: 50 usuários virtuais

RPS Média (Requisições por Segundo): ~20 req/s

Taxa de Erro: 0.0% (2.700+ requisições consecutivas sem falhas ou deadlocks)

-----

🚦 Como Rodar o Projeto<br>
Pré-requisitos <br>

Docker e Docker Compose instalados

Python 3.11+ e Poetry configurados

---------

Passo a Passo<br>
Clone o repositório:

Bash
git clone https://github.com/brunonativaa/nuclone-core-api.git
cd nuclone-core-api
Instale as dependências via Poetry:

Bash
poetry install
Suba o banco de dados PostgreSQL via Docker:

Bash
docker compose up -d
Inicie a aplicação FastAPI:

Bash
poetry run uvicorn src.main:app --reload
Acesse a documentação interativa:

Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

-----

🛡️ Decisões de Engenharia<br>

SGBD Relacional: Escolha do PostgreSQL pela robustez de ACID necessária em transações bancárias.

Isolamento de Testes: Utilização de mocks na camada HTTP/Router para garantir execução instantânea da suíte CI/CD e testes isolados no Locust com dados dinâmicos via zfill e timestamps.

Tratamento Fino de Exceções: Mapeamento direto de exceções customizadas de domínio (ContaNaoEncontradaException, SaldoInsuficienteException) para respostas HTTP semânticas.