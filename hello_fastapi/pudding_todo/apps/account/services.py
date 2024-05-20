from starlette.authentication import UnauthenticatedUser
from pydantic import SecretStr
from .models import User

class UserService:
    _data = {
        "puddingcamp": "PuddingCamp2024",
    }

    async def authenticate(self, username: str, password: SecretStr | str) -> User | UnauthenticatedUser:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()

        if self._data.get(username) != password:
            return UnauthenticatedUser()
        return User(username=username, password=SecretStr(password))
