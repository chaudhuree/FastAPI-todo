from pydantic import BaseModel

class TodoCreate(BaseModel):
    task: str
    status: str = "pending"


class TodoUpdate(BaseModel):
    task: str
    status: str


class TodoResponse(BaseModel):
    id: int
    task: str
    status: str