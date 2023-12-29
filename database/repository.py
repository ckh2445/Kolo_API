#함수를 통해 데이터베이스를 조회 
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm import ToDo

def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))

def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance = todo)
    session.commit() #db save
    session.refresh(instance = todo) #db read -> todo_id
    return todo