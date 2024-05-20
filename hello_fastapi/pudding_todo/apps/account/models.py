from pydantic import BaseModel, SecretStr
from starlette.authentication import BaseUser

class User(BaseUser, BaseModel):
    username: str
    password: SecretStr

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def identity(self) -> str:
        return self.username

