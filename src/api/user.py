from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler():
    # 1. request body(username, password)  별도의 중복 체크 x
    # 2. password -> hashing -> hashed_password
    # 3. User(username, hashed_password)
    # 4. user -> DB save
    # 5. return user(id, username)
    return True
