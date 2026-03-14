from pydantic import BaseModel

class todo(BaseModel):
    id: int
    task: str
    status: str
