from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://admin:admin@localhost:5433/todo_db"

engine = create_engine(DATABASE_URL)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()