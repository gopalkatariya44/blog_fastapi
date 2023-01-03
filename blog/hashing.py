from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        return pwd_context.verify(hashed_password, plain_password)
