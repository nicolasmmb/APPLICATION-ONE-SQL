"""Create Users Table

Revision ID: 48fa24973d26
Revises:
Create Date: 2021-11-12 11:58:36.168805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48fa24973d26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('nome', sa.String(96), nullable=False),
                    sa.Column('email', sa.String(255), unique=True, nullable=False),
                    sa.Column('cpf', sa.String(11), unique=True, nullable=False),
                    sa.Column('pis', sa.String(11), unique=True, nullable=False),
                    sa.Column('senha', sa.String(255), nullable=False),
                    # sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('address',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('pais', sa.String(64), nullable=False),
                    sa.Column('estado', sa.String(64), nullable=False),
                    sa.Column('municipio', sa.String(64), nullable=False),
                    sa.Column('cep', sa.String(8), nullable=False),
                    sa.Column('rua', sa.String(96), nullable=False),
                    sa.Column('numero', sa.Integer, nullable=False),
                    sa.Column('complemento', sa.String(255), nullable=False),
                    # Foreign Keys
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
                    sa.orm.relationship('Users', backref='address', cascade='all, delete-orphan')
                    )
    # alembic revision 48fa24973d26_create_users_table.py

    op.create_foreign_key(
        'user_id',
        source_table='address',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE',
    )
    pass


def downgrade():
    pass
