--- tentar deixar saldo negativo (violando CHECK)
BEGIN;
UPDATE saldo_conta
SET saldo_disponivel = saldo_disponivel - 999999
WHERE id_conta = 1;
COMMIT;