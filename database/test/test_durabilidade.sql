--- Garantir que, após COMMIT, os dados não desaparecem, mesmo após reiniciar o banco.
BEGIN;
UPDATE saldo_conta
SET saldo_disponivel = saldo_disponivel + 200
WHERE id_conta = 1;
INSERT INTO transacao (id_conta_origem, id_conta_destino, valor)
VALUES (NULL, 1, 200);
COMMIT;
--- Durabilidade OK