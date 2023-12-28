from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, Integer, String

Base = declarative_base()

class ToDo(Base):
    __tablename__ = 'todo'
    
    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    
    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_don={self.is_done}"
    
if __name__ == '__main__':
    from connection import SessionFactory
    from sqlalchemy import select
    from orm import ToDo
    
    session = SessionFactory()
    session.scalars(select(ToDo))
    todos = list(session.scalars(select(ToDo))) 
    
    for todo in todos:
        print(todo)