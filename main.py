from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# coming from database/db.py and database/base.py
from database.db import engine, get_db
from database.base import Base
from models.todo_model import Todo

from models.pydantic_todo_models import TodoCreate, TodoUpdate, TodoResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def server_status():
    return {
        "status": "running",
        "services": {
            "fastapi_server": "http://localhost:8000",
            "database_postgres": "localhost:5433",
            "pgadmin_ui": "http://localhost:5050"
        },
        "api_docs": {
            "swagger_ui": "http://localhost:8000/docs",
            "redoc": "http://localhost:8000/redoc"
        }
    }
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "FastAPI",
        "version": "1.0.0"
    }

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    db_todos = db.query(Todo).all()
    return {
        "message": "Todos retrieved successfully",
        "todos": [
            TodoResponse(id=item.id, task=item.task, status=item.status)
            for item in db_todos
        ],
    }

@app.get("/todos/paginated")
def get_paginated_todos(
    page: int = 1,
    size: int = 10,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Todo)
    if status:
        query = query.filter(Todo.status == status)

    total = query.count()
    db_todos = query.offset((page - 1) * size).limit(size).all()

    return {
        "message": "Todos retrieved successfully",
        "todos": [
            TodoResponse(id=item.id, task=item.task, status=item.status)
            for item in db_todos
        ],
        "total": total,
        "page": page,
        "size": size,
    }


@app.get("/todo/{id}")
def get_todo(id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {
        "message": "Todo retrieved successfully",
        "todo": TodoResponse(id=db_todo.id, task=db_todo.task, status=db_todo.status),
    }


@app.post("/todo")
def add_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(task=todo.task, status=todo.status)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {
        "message": "Todo added successfully",
        "todo": TodoResponse(id=new_todo.id, task=new_todo.task, status=new_todo.status),
    }


@app.put("/todo/{id}")
def update_todo(id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.task = updated_todo.task
    db_todo.status = updated_todo.status
    db.commit()
    db.refresh(db_todo)

    return {
        "message": "Todo updated successfully",
        "todo": TodoResponse(id=db_todo.id, task=db_todo.task, status=db_todo.status),
    }


@app.delete("/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    deleted = TodoResponse(id=db_todo.id, task=db_todo.task, status=db_todo.status)
    db.delete(db_todo)
    db.commit()

    return {"message": "Todo deleted successfully", "todo": deleted}