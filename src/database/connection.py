from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():  # generator 따로 학습 추가 필요할 듯
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
# session = SessionFactory()

# from sqlalchemy import select

# session.scalar(select(1))
