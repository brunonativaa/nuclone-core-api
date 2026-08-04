from src.core.database import SessionLocal
from src.services.cliente_service import (
    ClienteService,
    ClienteJaExisteException,
    ClienteNaoEncontradoException
)


def executar_testes_cliente():
    db = SessionLocal()
    try:
        service = ClienteService(db)

        print("\n--- TESTE 1: Criando Cliente ---")
        try:
            datas = {
                "nome": "Bruno Nativa",
                "cpf": "123.456.789-00",
                "email": "bruno@email.com",      # <--- Obrigatório (NOT NULL)
                "senha": "senha_criptografada",  # <--- Se for NOT NULL no banco
                "sexo": "M",
                "data_nascimento": "1997-08-15"  # <--- Se necessário
            }
            customer = service.create_customer(datas)
            print(
                f"Sucesso! Cliente criado ID: {customer.id_cliente} - Nome: {customer.nome}")
        except ClienteJaExisteException as e:
            print("Aviso:", e)

        print("\n--- TESTE 2: Tentando CPF Duplicado ---")
        try:
            dados_duplicados = {
                "nome": "Outro Bruno",
                "cpf": "123.456.789-00",
                "email": "outro_email@email.com",
                "senha": "outra_senha"
            }
            service.create_customer(dados_duplicados)
        except ClienteJaExisteException as e:
            print("Capturado com sucesso (CPF duplicado):", e)

        print("\n--- TESTE 3: Buscando Cliente por ID Inexistente ---")
        try:
            service.get_by_id(9999)
        except ClienteNaoEncontradoException as e:
            print("Capturado com sucesso (Cliente Inexistente):", e)

    finally:
        db.close()


if __name__ == "__main__":
    executar_testes_cliente()
