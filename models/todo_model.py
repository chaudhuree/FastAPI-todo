from sqlalchemy import Column, Integer, String
# coming from database/base.py
from database.base import Base 


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String)
    status = Column(String)