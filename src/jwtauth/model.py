# jwtauth/model.py
# Inspired by:
#   https://testdriven.io/blog/fastapi-jwt-auth/
#   https://docs.pydantic.dev/usage/schema/

from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from typing import Annotated
from os import getenv
from enum import Enum

# *** Environment Variables
# The file simulates a fake user database
USR_DATABASE = getenv('FAKEAPI_USR_DATABASE', 'users.json')
# The interface Uvicorn listens
HOSTNAME = getenv('FAKEAPI_INTF', '0.0.0.0')
# The TCP port for Uvicorn
PORT = int(getenv('FAKEAPI_PORT', 8000))

class Role(Enum):
    ADMIN = 'admin'
    SUPER = 'super'
    OPS = 'OPS'

class UserSchema(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    fullname: Annotated[str, Field(max_length=32)]
    email: EmailStr = Field(...)
    password: Annotated[str, Field(max_length=128)]
    role: Role

    class Config:
        schema_extra = {
            "example": {
                "id": "16fd2706-8baf-433b-82eb-8c7fada847da",
                "fullname": "Daniel Della-Noce",
                "email": "daniel@isociel.com",
                "password": "weakpassword"
            }
        }

class Email(BaseModel):
    email: EmailStr = Field(...)

class EmailPassword(BaseModel):
    email: EmailStr = Field(...)
    password: Annotated[str, Field(max_length=128)]


if __name__ == "__main__":
    import json
    # "BaseModel.schema" will return a dict of the schema,
    # "BaseModel.schema_json" will return a JSON string representation of that dict.

    # this is equivalent to json.dumps(UserSchema.schema(), indent=2)
    myString = UserSchema.schema_json(indent=2)
    print(UserSchema.schema_json(indent=2))    # type 'str'

    # this returns a Dict()
    myDict = UserSchema.schema()
    print(UserSchema.schema())  # type 'dict'

    print(f'\nType(myString)={type(myString)} - Type(myDict)={type(myDict)} - '
          f'Type(json.dumps(UserSchema.schema()))={type(json.dumps(UserSchema.schema()))}')
