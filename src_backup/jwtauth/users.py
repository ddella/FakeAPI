# jwtauth/users.py
"""
This module contains all the API related to users for authentication.
"""
from fastapi import APIRouter, HTTPException, status, Request
from jwtauth.model import UserSchema, Email
import jwtauth.database as db
# import the hash algorithm
from passlib.hash import pbkdf2_sha256


router = APIRouter()

@router.post("/api/user/signup", status_code=status.HTTP_201_CREATED, tags=["post"])
def create_user(user: UserSchema) -> dict:
    """
    Create a user in the "users" database for authentication of some endpoints.

    If the client makes a typo or sends a wrong key/value pair, the server will send a:
        HTTP/1.1 422 Unprocessable Entity

    curl -X POST -H "Content-type: application/json" -H "Accept: application/json" \
    -d '{"id": "1b702cc8-4e71-4685-bc48-df62a8205fd7","fullname": "User3 Name3","email": "user3@example.com","password": "Password3"}' \
    -i -L "http://localhost:8000/api/user/signup"

    curl -X POST -H "Content-type: application/json" -H "Accept: application/json" \
    -d '{"id": "a8098c1a-f86e-11da-bd1a-00112444be1e","fullname": "User5 Name5","email": "user5@example.com","password": "Password5"}' \
    -i -L "http://localhost:8000/api/user/signup"

    :param user: The new user to add to the user's database
    :return: The newly created user is returned
    """
    users = db.readUsrData()
    record = [d for d in users if d.email == user.email]
    if record:
        # record is a list with only one element, if ID is unique 😉
        strError = f"ID {user.email} already exists, adding item failed"
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=strError,
            headers={"X-Fake-REST-API": strError},
        )
    # hash the password before saving to the database
    user.password = pbkdf2_sha256.hash(user.password)
    users.append(user)
    db.writeUsrData(users)
    return dict(user)

@router.get("/api/users", tags=["get"])
async def all_users(request: Request) -> dict:
    """
    Returns all the users. No parameter needed.

    curl -H "Content-type: application/json" -H "Accept: application/json" -i -L  http://localhost:8000/api/users

    :return: All the elements
    """
    users = db.readUsrData()
    return {"message": "Users database", "method": request.method, "users": users}

@router.get("/api/user/email", status_code=status.HTTP_200_OK, tags=["content_parameter"])
async def user_email(user_email: Email) -> dict:
    """
    This API returns all the information of a user specified by its email address.

    Example with curl:
        curl -X GET -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"email": "user3@example.com"}' -i -L "http://localhost:8000/api/user/email"
    :param user_email: The email address of the user we want to retreive
    :return: The user or error 404 if not found
    """
    users = db.readUsrData()
    record = [d for d in users if d.email == user_email.email]
    if record:
        # record is a list with only one element, if email is unique 😉
        return {"user": record[0]}

    strError = f"User with email {user_email.email} was not found"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )


if __name__ == "__main__":
    import uvicorn
    import logging
    import platform
    from model import HOSTNAME, PORT
    from fastapi import FastAPI

    # logger config
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s %(funcName)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f'Python version: {platform.python_version()}')
    logging.info(f'Hostname: {platform.node()}')

    app = FastAPI()
    app.include_router(router)

    uvicorn.run(app, host=HOSTNAME, port=PORT, log_level="info")
