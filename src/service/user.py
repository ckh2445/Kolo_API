import bcrypt


class UserService:
    encoding: str = "UTF-8"

    def hast_password(self, plain_password: str) -> str:  # 해쉬값은 byte
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt(),
        )

        return hashed_password.decode(self.encoding)
