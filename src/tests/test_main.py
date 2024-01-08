from fastapi.testclient import TestClient

from database.orm import ToDo
from main import app

client = TestClient(app=app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(mocker):
    # order=ASC
    '''
    test 코드 작성은 실제 DB에 요청을 여러번 하는것보다 적게 하는게 좋다  (연산이 오래걸린다)
    그러므로 mocking을 사용한다
    외부 api 또는 db에서 꺼내오는 작업은 오래 걸리는 연산이다 이를 목킹을 사용한다.
    data가 많다면 테스트코드가 오래걸린다.
    '''
    mocker.patch("main.get_todos", return_value =[
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ])
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
        ]
    }

    #order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        ]
    }
