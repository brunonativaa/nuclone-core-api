-- 1. Inserindo Clientes (Mariana e Carlos)
INSERT INTO cliente (nome, cpf, sexo, email, senha, data_nascimento)
VALUES (
        'Carlos Souza',
        '111.222.333-44',
        'M',
        'carlos@nuclone.com',
        'hash_senha_1',
        '1990-04-12'
    ),
    (
        'Mariana Rocha',
        '555.666.777-88',
        'F',
        'mariana@nuclone.com',
        'hash_senha_2',
        '1998-09-21'
    );
-- 2. Inserindo Telefones
INSERT INTO telefone (id_cliente, numero, tipo)
VALUES (1, '(11) 99999-1111', 'CELULAR'),
    (2, '(21) 98888-2222', 'CELULAR');
-- 3. Inserindo Endereços
INSERT INTO endereco (
        id_cliente,
        estado,
        cidade,
        bairro,
        rua,
        cep,
        num
    )
VALUES (
        1,
        'SP',
        'São Paulo',
        'Pinheiros',
        'Av. Brigadeiro Faria Lima',
        '01451001',
        '3500'
    ),
    (
        2,
        'RJ',
        'Rio de Janeiro',
        'Copacabana',
        'Avenida Atlântica',
        '22070011',
        '1500'
    );
-- 4. Inserindo as Contas Bancárias (id_cliente 1 e 2)
INSERT INTO conta (id_cliente, num_conta, tipo_conta, agencia)
VALUES (1, '00001234-5', 'PF', '0001'),
    -- Conta do Carlos
    (2, '00005678-9', 'PF', '0001');
-- Conta da Mariana
-- 5. Inicializando os Saldos das Contas
INSERT INTO saldo_conta (id_conta, saldo_disponivel, saldo_bloqueado)
VALUES (1, 1000.00, 0.00),
    -- Carlos começa com R$ 1.000,00
    (2, 50.00, 0.00);
-- Mariana começa com R$ 50,00