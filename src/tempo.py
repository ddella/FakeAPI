"""
Convert data from a Pydantic model in another Pydantic model.
https://fastapi.tiangolo.com/tutorial/extra-models/

Results:
src = username='Daniel' age=55 role='admin' - id(src) = 4369494032
dst = uuid=123456 username='Daniel' age=55 role='admin' - id(dst) = 4357523216
"""
from pydantic import BaseModel

class Source(BaseModel):
    username: str
    age: int
    role: str

class Destination(BaseModel):
    uuid: int
    username: str
    age: int
    role: str


src: Source = Source(username='Daniel', age=55, role='admin')
dst: Destination = Destination(**src.dict(), uuid=123456)

print(f'src = {src} - id(src) = {id(src)}')
print(f'dst = {dst} - id(dst) = {id(dst)}')
