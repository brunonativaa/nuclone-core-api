-- 1. TABELA CLIENTE
CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(15) NOT NULL UNIQUE,
    sexo CHAR(1),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(60) NOT NULL,
    data_nascimento DATE NOT NULL
);
-- 2. TABELA TELEFONE
CREATE TABLE telefone (
    id_telefone SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    numero VARCHAR(15) NOT NULL,
    tipo tipo_num NOT NULL DEFAULT 'CELULAR'
);
-- 3. TABELA ENDERECO
CREATE TABLE endereco (
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
CREATE TABLE conta (
    id_conta SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    num_conta VARCHAR(20) UNIQUE NOT NULL,
    tipo_conta tipo_conta NOT NULL DEFAULT 'PF',
    agencia VARCHAR(10) NOT NULL
);
CREATE TABLE saldo_conta (
    id_saldo_conta SERIAL PRIMARY KEY,
    id_conta INTEGER UNIQUE NOT NULL,
    saldo_disponivel DECIMAL(15, 2) NOT NULL CHECK (saldo_disponivel >= 0.00),
    saldo_bloqueado DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE transacao (
    id_transacao SERIAL PRIMARY KEY,
    id_conta_origem INTEGER NOT NULL,
    id_conta_destino INTEGER NOT NULL,
    tipo_transacao tipo_transacao NOT NULL DEFAULT 'PIX',
    valor DECIMAL (15, 2) NOT NULL CHECK (valor > 0.00),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)