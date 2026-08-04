from src.core.database import SessionLocal
from src.services.pix_service import (
    PixService,
    SaldoInsuficienteException,
    ContaNaoEncontradaException
)


def executar_testes_pix():
    db = SessionLocal()
    try:
        service = PixService(db)

        # Substitua pelos IDs de contas válidas do seu banco de dados
        CONTA_ORIGEM = 1
        CONTA_DESTINO = 2

        print("--- TESTE 1: Realizando Pix com sucesso ---")
        resultado = service.realizar_pix(
            id_conta_origem=CONTA_ORIGEM,
            id_conta_destino=CONTA_DESTINO,
            valor=50.00
        )
        print("Sucesso! Transação gravada:", resultado)

        print("\n--- TESTE 2: Tentando Pix sem saldo ---")
        try:
            service.realizar_pix(
                id_conta_origem=CONTA_ORIGEM,
                id_conta_destino=CONTA_DESTINO,
                valor=9999999.00
            )
        except SaldoInsuficienteException as e:
            print("Capturado com sucesso (Saldo Insuficiente):", e)

        print("\n--- TESTE 3: Tentando Pix para conta inexistente ---")
        try:
            service.realizar_pix(
                id_conta_origem=CONTA_ORIGEM,
                id_conta_destino=9999,
                valor=10.00
            )
        except ContaNaoEncontradaException as e:
            print("Capturado com sucesso (Conta Inexistente):", e)

    finally:
        db.close()


if __name__ == "__main__":
    executar_testes_pix()
