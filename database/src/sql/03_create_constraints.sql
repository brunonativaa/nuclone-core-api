ALTER TABLE cliente
ADD CONSTRAINT chk_maior_de_idade CHECK (
        data_nascimento <= CURRENT_DATE - INTERVAL '18 years'
    );
ALTER TABLE telefone
ADD CONSTRAINT telefone_id_client_fk FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE;
ALTER TABLE endereco
ADD CONSTRAINT endereco_id_cliente_fk FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE;
ALTER TABLE conta
ADD CONSTRAINT conta_id_cliente_fk FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE;
ALTER TABLE saldo_conta
ADD CONSTRAINT saldo_conta_id_conta_fk FOREIGN KEY (id_conta) REFERENCES conta(id_conta) ON DELETE CASCADE;
ALTER TABLE transacao
ADD CONSTRAINT transacao_id_conta_origem_fk FOREIGN KEY (id_conta_origem) REFERENCES conta(id_conta) ON DELETE CASCADE;
ALTER TABLE transacao
ADD CONSTRAINT transacao_id_conta_destino_fk FOREIGN key (id_conta_destino) REFERENCES conta(id_conta) ON DELETE CASCADE;