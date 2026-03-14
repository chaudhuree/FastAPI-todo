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
def greet():
    return {"message": "This is a simple todo app built with FastAPI"}


@app.get("/todos")
def get_todos():
    return { "message": "Todos retrieved successfully","todos": todos,}

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