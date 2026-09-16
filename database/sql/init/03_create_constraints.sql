ALTER TABLE
    clientes
ADD
    CONSTRAINT chk_maior_de_idade CHECK (
        data_nascimento <= CURRENT_DATE - INTERVAL '18 years'
    );

ALTER TABLE
    clientes
ADD
    CONSTRAINT cpf_11_digitos CHECK (
        char_length(cpf) = 11
        AND cpf ~ '^[0-9]+$'
    );

ALTER TABLE
    telefones
ADD
    CONSTRAINT telefones_id_client_fk FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE;

ALTER TABLE
    telefones
ADD
    CONSTRAINT telefones_numerico CHECK (numero ~ '^[0-9]+$');

ALTER TABLE
    enderecos
ADD
    CONSTRAINT enderecos_id_cliente_fk FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE;

ALTER TABLE
    enderecos
ADD
    CONSTRAINT cep_8_digitos CHECK (
        char_length(cep) = 8
        AND cep ~ '^[0-9]+$'
    );

ALTER TABLE
    contas
ADD
    CONSTRAINT contas_id_cliente_fk FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE;

ALTER TABLE
    saldo_contas
ADD
    CONSTRAINT saldo_contas_id_conta_fk FOREIGN KEY (id_conta) REFERENCES contas(id_conta) ON DELETE CASCADE;

ALTER TABLE
    limites_contas
ADD
    CONSTRAINT limites_contas_id_conta_fk FOREIGN KEY (id_conta) REFERENCES contas(id_conta) ON DELETE CASCADE;

ALTER TABLE
    chaves_pix
ADD
    CONSTRAINT chaves_pix_id_conta_fk FOREIGN KEY (id_conta) REFERENCES contas(id_conta) ON DELETE CASCADE;

ALTER TABLE
    transacao
ADD
    CONSTRAINT transacao_id_conta_origem_fk FOREIGN KEY (id_conta_origem) REFERENCES contas(id_conta) ON DELETE CASCADE;

ALTER TABLE
    transacao
ADD
    CONSTRAINT transacao_id_conta_destino_fk FOREIGN key (id_conta_destino) REFERENCES contas(id_conta) ON DELETE CASCADE;