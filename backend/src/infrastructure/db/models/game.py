import uuid
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from infrastructure.db.session import Base


class GameModel(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_move_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    board = Column(JSON, nullable=False)
    rows = Column(Integer, nullable=False)
    cols = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False, default=0)
    target_score = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")

    one_swap_reset = Column(Boolean, nullable=False, default=False)
    random_item_mode = Column(Boolean, nullable=False, default=False)
    random_item = Column(String, nullable=True)
    items_count = Column(Integer, nullable=False, default=6)
    timeout_seconds = Column(Integer, nullable=False, default=3600)
    player = Column(String, nullable=False, default="player")
