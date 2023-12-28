# response schema 정의

from typing import List
from pydantic import BaseModel

# 현재는 단순한 db지만 향 후 커지게되어 db 연산이나 중첩되는 구조아니면 컨텐츠의 값 즉 특정 key를 제거하여 response할 때 필요하여 분리작업이 필요
class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool
    
    class Config:
        orm_mode = True
    
class ListToDoResponse(BaseModel):
    todos: List[ToDoSchema]
    
    
if __name__ == "__main__":
    from schema.response import ToDoSchema
    from database.orm import ToDo
    
    todo = ToDo(id=100, contents="test", is_done=True)
    
    ToDoSchema.from_orm(todo)
    

