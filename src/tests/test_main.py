from fastapi.testclient import TestClient

from database.orm import ToDo

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(client, mocker):
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

def test_get_todo(client, mocker):
    #200
    mocker.patch(
                 "main.get_todo_by_todo_id",
                 return_value=ToDo(id=1, contents="FastAPI Section 0", is_done=True),
                 )
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "FastAPI Section 0", "is_done": True}

    #404
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=None,
    )
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not Found"}

def test_create_todo(client, mocker):
    '''
    단순 mocking을 사용할 경우 main.py의 51번째 줄을 테스트하지 못한다.
    spy라는 기능을 이용하여 특정 개체를 tracking을 할 수 있다. 하지만 equal mathcing method를 overriding할 수 있지만 현재는 어려운 개념이므로 pass
    '''
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch(
        "main.create_todo",
        return_value=ToDo(id=1, contents="todo", is_done=True),
    )
    body = {
        "contents":"test",
        "is_done":False,
    }
    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None #이 시점에서는 orm객체가 생성이 되었지만 id가 없음
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}