from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from cache import redis_client
from database.orm import User
from database.repository import UserRepository
from schema.request import SignUpRequest, LogInRequest, CreateOTPRequest, VerifyOTPRequest
from schema.response import UserSchema, JWTResponse
from security import get_access_token
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
    user: User = user_repo.save_user(user=user)  # id= int

    # 5. return user(id, username)
    return UserSchema.from_orm(user)


@router.post("/log-in")
def user_log_in_handler(
        request: LogInRequest,
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. request body(username, password)
    # 2. db read user
    user: User | None = user_repo.get_user_by_username(
        username=request.username
    )
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    # 3. user.password, request.password -> bcrypt.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    )

    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")  # 일반적으로 인증 실패 시 401

    # 4. create jwt
    access_token: str = user_service.create_jwt(username=user.username)

    # 5. return jwt
    return JWTResponse(access_token=access_token)


# 회원가입(username, password)/ 로그인
# 이메일 알림: 회원가입 -> 이메일 인증(otp) -> 유저 이메일 저장 -> 이메일 알림

# POST /users/email/otp -> (key: email, value: 1234, exp: 3min)
# POST /users/email/otp/verify -> request(email, otp) -> user(email)

@router.post("/email/otp")
def create_otp_handler(
        request: CreateOTPRequest,
        _: str = Depends(get_access_token),  # header 검증 사용하진 않음
        user_service: UserService = Depends(),

):
    # 1. access_token - 회원 가입 완료된 회원만 이메일 인증
    # 2. request body(email)
    # 3. otp create(random 4 digit)
    otp: int = user_service.create_otp()

    # 4. redis otp(email, 1234, exp=3min)
    redis_client.set(request.email, otp)
    redis_client.expire(request.email, 3 * 60)

    # 5. send otp to email
    return {"otp": otp}


@router.post("/email/otp/verify")
def verify_otp_handler(
        request: VerifyOTPRequest,
        background_tasks: BackgroundTasks,
        access_token: str = Depends(get_access_token),
        user_service: UserService = Depends(),
        user_repo: UserRepository = Depends(),
):
    # 1. access_token
    # 2. request body(email, otp)
    otp: str | None = redis_client.get(request.email)

    if not otp:
        raise HTTPException(status_code=400, detail="Bad Request")

    if request.otp != int(otp):
        raise HTTPException(status_code=400, detail="Bad Request")

    # 3. request.otp == redis.get(email)
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=400, detail="User Not Found")

    # save email to user
    # 4. user(email)
    # send email to user
    # 시간이 오래걸리기 때문에 background에서 돌아야한다. 그것이 바로 background test
    background_tasks.add_task(
        user_service.send_email_to_user,
        email="st@fastapi.com"
    )
    return UserSchema.from_orm(user)
    #server Request -> verify_otp -> send email(10s) -> Response
    # Background                                                -> send email(10s)
