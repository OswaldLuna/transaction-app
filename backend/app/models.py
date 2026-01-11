from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from datetime import datetime, timezone
from app.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="pendiente")
    hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AssistantLog(Base):
    __tablename__ = "assistant_logs"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=False)
