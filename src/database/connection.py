from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:kolotodos2@158.179.171.103:31259/todos"

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():  # generator 따로 학습 추가 필요할 듯
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
