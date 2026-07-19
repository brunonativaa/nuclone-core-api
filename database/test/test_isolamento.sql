BEGIN;
SELECT saldo_disponivel
FROM saldo_conta
WHERE id_conta = 1 FOR
UPDATE;
-- bloqueia a linha
--- Sessão A segura o lock
BEGIN;
UPDATE saldo_conta --- Sessão B ao mesmo tempo
SET saldo_disponivel = saldo_disponivel - 50
WHERE id_conta = 1;
--- Sessão B fica esperando (não trava, não erra, só espera).
UPDATE saldo_conta -- Sessão A finaliza
SET saldo_disponivel = saldo_disponivel - 100
WHERE id_conta = 1;
COMMIT;
-- Quando o lock é liberado, Sessão B executa sua operação.
SELECT saldo_disponivel
FROM saldo_conta
WHERE id_conta = 1;
-- Saldo deve refletir ambas operações, sem conflito → Isolamento OK.