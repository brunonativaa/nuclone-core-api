-- 01_create_types.sql
-- Tipos enumerados para o ecossistema NuClone Core API

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_num') THEN
        CREATE TYPE tipo_num AS ENUM ('CELULAR', 'RESIDENCIAL', 'COMERCIAL');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_de_conta') THEN
        CREATE TYPE tipo_de_conta AS ENUM ('PF', 'PJ');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_de_transacao') THEN
        CREATE TYPE tipo_de_transacao AS ENUM ('PIX', 'TED', 'DOC', 'ESTORNO');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_de_status') THEN
        CREATE TYPE tipo_de_status AS ENUM ('CONCLUIDO', 'PENDENTE', 'ESTORNADO', 'CANCELADO', 'FALHOU');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_chave_pix') THEN
        CREATE TYPE tipo_chave_pix AS ENUM ('CPF', 'EMAIL', 'TELEFONE', 'ALEATORIA');
    END IF;
END $$;