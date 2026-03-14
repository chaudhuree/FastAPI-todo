from fastapi import FastAPI

from todo_models import todo

app = FastAPI()

# In-memory storage for todos
todos = [
    todo(id=1, task="Buy groceries", status="pending"),
    todo(id=2, task="Clean the house", status="pending"),
    todo(id=3, task="Finish homework", status="pending")
]


@app.get("/")
def serverStatus():
    return {"message": "This is a simple todo app built with FastAPI and the server is running on port 8000."}


@app.get("/todos")
def get_todos():
    return { "message": "Todos retrieved successfully","todos": todos,}

# todos with pagination and filtering by status . Example: /todos/paginated?page=1&size=2&status=pending
@app.get("/todos/paginated")
def get_todos_paginated(page: int = 1, size: int = 10, status: str = None):
    filtered_todos = [todo for todo in todos if status is None or todo.status == status]
    start = (page - 1) * size
    end = start + size
    return {
        "message": "Todos retrieved successfully",
        "todos": filtered_todos[start:end],
        "total": len(filtered_todos),
        "page": page,
        "size": size,
    }

@app.get("/todo/{id}")
def getTodo(id: int):
    for todo in todos:
        if todo.id == id:
            return {"message": "Todo retrieved successfully", "todo": todo}
    return {"message": "Todo not found"}

@app.post("/todo")
def addTodo(todo: todo):
    todos.append(todo)
    return {"message": "Todo added successfully", "todo": todo}

@app.put("/todo/{id}")
def updateTodo(id: int, updated_todo: todo):
    for index, todo in enumerate(todos):
        if todo.id == id:
            todos[index] = updated_todo
            return {"message": "Todo updated successfully", "todo": updated_todo}
    return {"message": "Todo not found"}

@app.delete("/todo/{id}")
def deleteTodo(id: int):
    for index, todo in enumerate(todos):
        if todo.id == id:
            deleted_todo = todos.pop(index)
            return {"message": "Todo deleted successfully", "todo": deleted_todo}
    return {"message": "Todo not found"}