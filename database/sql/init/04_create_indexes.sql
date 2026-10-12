CREATE INDEX IF NOT EXISTS idx_transacao_origem_data ON transacao(id_conta_origem, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transacao_destino_data ON transacao(id_conta_destino, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chaves_pix_valor ON chaves_pix(valor_chave);
CREATE INDEX IF NOT EXISTS idx_auth_credenciais_cliente ON auth_credenciais(id_cliente);
CREATE INDEX IF NOT EXISTS idx_transacao_limites_janela 
ON transacao(id_conta_origem, status, is_noturno, created_at);