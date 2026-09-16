-- 1. TABELA CLIENTE
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    sexo CHAR(1),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    pin_transacao_hash VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABELA TELEFONE
CREATE TABLE telefones (
    id_telefone SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    numero VARCHAR(15) NOT NULL,
    tipo tipo_num NOT NULL DEFAULT 'CELULAR'
);

-- 3. TABELA ENDERECO
CREATE TABLE enderecos (
    id_endereco SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    rua VARCHAR(150) NOT NULL,
    cep VARCHAR(8) NOT NULL,
    num VARCHAR(10) NOT NULL
);

-- 4. TABELA CONTA
CREATE TABLE contas (
    id_conta SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    num_conta VARCHAR(20) UNIQUE NOT NULL,
    tipo_conta tipo_de_conta NOT NULL DEFAULT 'PF',
    agencia VARCHAR(10) NOT NULL DEFAULT '0001',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE saldo_contas (
    id_saldo_conta SERIAL PRIMARY KEY,
    id_conta INTEGER UNIQUE NOT NULL,
    saldo_disponivel DECIMAL(15, 2) NOT NULL CHECK (saldo_disponivel >= 0.00),
    saldo_bloqueado DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE limites_contas (
    id_limite SERIAL PRIMARY KEY,
    id_conta INTEGER UNIQUE NOT NULL,
    limite_diario DECIMAL(15, 2) NOT NULL DEFAULT 5000.00 CHECK (limite_diario >= 0.00),
    limite_noturno DECIMAL(15, 2) NOT NULL DEFAULT 1000.00 CHECK (limite_noturno >= 0.00),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chaves_pix (
    id_chave SERIAL PRIMARY KEY,
    id_conta INT NOT NULL,
    tipo_chave tipo_chave_pix NOT NULL,
    valor_chave VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_chaves_pix_conta FOREIGN KEY (id_conta) REFERENCES contas(id_conta) ON DELETE CASCADE
);

CREATE TABLE transacao (
    id_transacao SERIAL PRIMARY KEY,
    id_conta_origem INTEGER NOT NULL,
    id_conta_destino INTEGER NOT NULL,
    tipo_transacao tipo_de_transacao NOT NULL DEFAULT 'PIX',
    valor DECIMAL (15, 2) NOT NULL CHECK (valor > 0.00),
    status tipo_de_status NOT NULL DEFAULT 'CONCLUIDO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transacao_origem_data ON transacao(id_conta_origem, created_at DESC);

CREATE INDEX idx_transacao_destino_data ON transacao(id_conta_destino, created_at DESC);

CREATE INDEX idx_chaves_pix_valor ON chaves_pix(valor_chave);