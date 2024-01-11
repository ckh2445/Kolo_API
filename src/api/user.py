from fastapi import APIRouter, Depends

from database.orm import User
from database.repository import UserRepository
from schema.request import SignUpRequest
from schema.response import UserSchema
from service.user import UserService

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. request body(username, password)  별도의 중복 체크 x
    # 2. password -> hashing -> hashed_password
    hashed_password: str = user_service.hash_password(
        plain_password=request.password
    )

    # 3. User(username, hashed_password)
    user: User = User.create(
        username=request.username, hashed_password=hashed_password,
    )

    # 4. user -> DB save
    user: User = user_repo.save_user(user=user) #id= int

    # 5. return user(id, username)
    return True
