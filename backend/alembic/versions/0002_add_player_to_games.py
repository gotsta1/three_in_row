from alembic import op
import sqlalchemy as sa

revision = "0002_add_player_to_games"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("games", sa.Column("player", sa.String(), nullable=False, server_default="player"))
    op.alter_column("games", "player", server_default=None)


def downgrade():
    op.drop_column("games", "player")
