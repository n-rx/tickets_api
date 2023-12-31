"""Init Migration

Revision ID: 91806d1519bf
Revises: 
Create Date: 2023-10-12 08:32:47.126870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '91806d1519bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('open', 'answered', 'waiting_answer', 'closed', name='ticket_status'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_comment',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('ticket_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket_comment')
    op.drop_table('ticket')
    # ### end Alembic commands ###
