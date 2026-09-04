-- 1. Inserindo Clientes (Carlos e Mariana)
INSERT INTO
    cliente (nome, cpf, sexo, email, senha, data_nascimento)
VALUES
    (
        'Carlos Souza',
        '11122233344',
        'M',
        'carlos@nuclone.com',
        'hash_senha_1',
        '1990-04-12'
    ),
    (
        'Mariana Rocha',
        '55566677788',
        'F',
        'mariana@nuclone.com',
        'hash_senha_2',
        '1998-09-21'
    );

-- 2. Inserindo Telefones
INSERT INTO
    telefone (id_cliente, numero, tipo)
VALUES
    (
        (
            SELECT
                id_cliente
            FROM
                cliente
            WHERE
                cpf = '11122233344'
        ),
        '11999995111',
        'CELULAR'
    ),
    (
        (
            SELECT
                id_cliente
            FROM
                cliente
            WHERE
                cpf = '55566677788'
        ),
        '21988883222',
        'CELULAR'
    );

-- 3. Inserindo Endereços
INSERT INTO
    endereco (
        id_cliente,
        estado,
        cidade,
        bairro,
        rua,
        cep,
        num
    )
VALUES
    (
        (
            SELECT
                id_cliente
            FROM
                cliente
            WHERE
                cpf = '11122233344'
        ),
        'SP',
        'São Paulo',
        'Pinheiros',
        'Av. Brigadeiro Faria Lima',
        '01451001',
        '3500'
    ),
    (
        (
            SELECT
                id_cliente
            FROM
                cliente
            WHERE
                cpf = '55566677788'
        ),
        'RJ',
        'Rio de Janeiro',
        'Copacabana',
        'Avenida Atlântica',
        '22070011',
        '1500'
    );

-- 4. Inserindo as Contas Bancárias
INSERT INTO
    conta (id_cliente, num_conta, tipo_conta, agencia)
VALUES
    (
        (
            SELECT
                id_cliente
            FROM
                cliente
            WHERE
                cpf = '11122233344'
        ),
        '00001234-5',
        'PF',
        '0001'
    ),
    (
        (
            SELECT
                id_cliente
            FROM
                cliente
            WHERE
                cpf = '55566677788'
        ),
        '00005678-9',
        'PF',
        '0001'
    );

-- 5. Inicializando os Saldos das Contas (Buscando o id_conta pela num_conta)
INSERT INTO
    saldo_conta (
        id_conta,
        saldo_disponivel,
        saldo_bloqueado,
        ultima_atualizacao
    )
VALUES
    -- Carlos começa com R$ 1.000,00
    (
        (
            SELECT
                id_conta
            FROM
                conta
            WHERE
                num_conta = '00001234-5'
        ),
        1000.00,
        0.00,
        NOW()
    ),
    -- Mariana começa com R$ 50,00 (Ajustado para 50.00 conforme o comentário)
    (
        (
            SELECT
                id_conta
            FROM
                conta
            WHERE
                num_conta = '00005678-9'
        ),
        50.00,
        0.00,
        NOW()
    );