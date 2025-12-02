from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "games",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.Column("last_move_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("board", sa.JSON(), nullable=False),
        sa.Column("rows", sa.Integer(), nullable=False),
        sa.Column("cols", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("target_score", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("one_swap_reset", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("random_item_mode", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("random_item", sa.String(), nullable=True),
        sa.Column("items_count", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("timeout_seconds", sa.Integer(), nullable=False, server_default="3600"),
    )

    op.create_table(
        "leaderboard",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("game_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("games.id", ondelete="CASCADE"), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("player", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table("leaderboard")
    op.drop_table("games")
