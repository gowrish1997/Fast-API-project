from sqlalchemy import Column, Integer, String, Boolean,DateTime
from app.database.db import Base
from datetime import datetime,timezone
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    content = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False,nullable=False)
    created_at = Column(DateTime, nullable=False,default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False,default=datetime.now(timezone.utc))
    