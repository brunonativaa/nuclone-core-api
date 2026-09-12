FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false

# Copia e instala apenas as dependências primeiro (aproveita o cache de camadas do Docker)
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --no-interaction

# Copia o restante do código
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
