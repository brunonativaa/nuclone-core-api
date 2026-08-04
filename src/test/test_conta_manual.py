from src.core.database import SessionLocal
from src.services.conta_service import (
    ContaService,
    ClienteNaoEncontradoException,
    ContaNaoEncontradaException
)


def executar_testes_conta():
    db = SessionLocal()
    try:
        service = ContaService(db)

        # ID de cliente real cadastrado no banco (ex: 55 do teste anterior)
        ID_CLIENTE_VALIDO = 55

        print("\n--- TESTE 1: Criando Conta para Cliente Válido ---")
        try:
            dados = {
                "id_cliente": ID_CLIENTE_VALIDO,
                "tipo_conta": "PF"
            }
            conta = service.create_account(dados)
            print(
                f"Sucesso! Conta criada ID: {conta.id_conta} - Num: {conta.num_conta}")
        except ClienteNaoEncontradoException as e:
            print("Erro:", e)

        print("\n--- TESTE 2: Consultando Saldo da Conta ---")
        try:
            saldo_info = service.get_saldo(conta.id_conta)
            print(f"Saldo disponível: R$ {saldo_info.saldo_disponivel}")
        except ContaNaoEncontradaException as e:
            print("Erro:", e)

        print("\n--- TESTE 3: Tentando criar conta para cliente inexistente ---")
        try:
            service.create_account({"id_cliente": 9999})
        except ClienteNaoEncontradoException as e:
            print("Capturado com sucesso (Cliente Inexistente):", e)

    finally:
        db.close()


if __name__ == "__main__":
    executar_testes_conta()
