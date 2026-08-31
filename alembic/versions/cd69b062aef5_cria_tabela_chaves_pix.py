"""cria_tabela_chaves_pix

Revision ID: <MANTENHA_O_HASH_GERADO_NO_ARQUIVO>
Revises: 52c934f23401
Create Date: 2026-08-31
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Identificadores de revisão do Alembic
revision: str = '<MANTENHA_O_HASH_GERADO_NO_ARQUIVO>'
down_revision: Union[str, Sequence[str], None] = '52c934f23401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Criação da Tabela chaves_pix
    op.create_table(
        'chaves_pix',
        sa.Column('id_chave', sa.Integer(),
                  autoincrement=True, nullable=False),
        sa.Column('id_conta', sa.Integer(), nullable=False),
        sa.Column(
            'tipo_chave',
            sa.Enum('CPF', 'EMAIL', 'TELEFONE',
                    'ALEATORIA', name='typechaveenum'),
            nullable=False
        ),
        sa.Column('valor_chave', sa.String(length=255), nullable=False),
        sa.Column(
            'criado_em',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ['id_conta'], ['conta.id_conta'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_chave')
    )

    # 2. Criação do índice único para o valor da chave Pix
    op.create_index(
        op.f('ix_chaves_pix_valor_chave'),
        'chaves_pix',
        ['valor_chave'],
        unique=True
    )


def downgrade() -> None:
    # Reverte as alterações caso precise dar rollback
    op.drop_index(op.f('ix_chaves_pix_valor_chave'), table_name='chaves_pix')
    op.drop_table('chaves_pix')
    op.execute("DROP TYPE IF EXISTS typechaveenum;")
