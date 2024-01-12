from datetime import datetime, timedelta
from random import random

import bcrypt
from jose import jwt


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "6b0698748fdd0d0ed38fcc6c239c06115c2dafcd859a6374055cb04f7ab073a6"  # openssl rand -hex 32 data
    jwt_algorithm: str = "HS256"

    def hash_password(self, plain_password: str) -> str:  # 해쉬값은 byte
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt(),
        )

        return hashed_password.decode(self.encoding)

    # 로그인검증
    def verify_password(
            self, plain_password: str, hashed_password: str
    ) -> bool:
        # try/except 문의 예외 처리가능

        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    # jwt 생성
    def create_jwt(self, username: dict) -> str:
        return jwt.encode(
            {
                "sub": username, # unique 식별자
                "exp": datetime.now() + timedelta(days=1)
            },
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def decode_jwt(self, access_token: str):
        payload: dict = jwt.decode(
            access_token,self.secret_key, algorithms=[self.jwt_algorithm]
        )
        # expire
        return payload["sub"] #username


    @staticmethod
    def create_otp() -> int:
        return random.randint(1000,9999)