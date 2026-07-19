UPDATE saldo_conta
SET saldo_disponivel = saldo_disponivel - 100
WHERE id_conta = 1;
UPDATE saldo_conta
SET saldo_disponivel = saldo_disponivel + 100
WHERE id_conta = 9999;
-- NÃO EXISTE
-- 3. Registra transação
INSERT INTO transacao (id_conta_origem, id_conta_destino, valor)
VALUES (1, 9999, 100);
COMMIT;