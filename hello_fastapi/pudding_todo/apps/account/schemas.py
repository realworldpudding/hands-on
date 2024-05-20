from pydantic import BaseModel, SecretStr, Field


class LoginSchema(BaseModel):
    username: str = Field(min_length=4)
    password: SecretStr = Field(min_length=8)

