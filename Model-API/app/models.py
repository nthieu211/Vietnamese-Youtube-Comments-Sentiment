from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    videoId = Column(String, index=True)
    username = Column(String, index=True)
    comment = Column(String, index=True)
    sentiment = Column(String, index=True)
    like = Column(Integer, index=True)
    timeCommented = Column(DateTime, index=True)
    timeCreated_inDB = Column(DateTime(timezone=True), server_default=func.now())
