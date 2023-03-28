# jwtauth/users.py
"""
This module contains all the API related to users authentication using JWT.
"""
import uuid

from fastapi import APIRouter, HTTPException, status, Request
from jwtauth.model import UserSchema, Email, EmailPassword
import jwtauth.database as db
from passlib.hash import pbkdf2_sha256

router = APIRouter()

@router.post("/api/user/signup", status_code=status.HTTP_201_CREATED, tags=["post"])
def create_user(user: UserSchema) -> dict:
    """
    TODO: https://fastapi.tiangolo.com/tutorial/extra-models/
    Create a user in the "users" database for authentication of some endpoints.

    If the client makes a typo or sends a wrong key/value pair, the server will send a:
        HTTP/1.1 422 Unprocessable Entity

    Example with curl:

        curl -X POST -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"fullname": "User3 Name3","email": "user3@example.com",\
        "password": "Password3", "role": "admin"}' -i -L "http://localhost:8000/api/user/signup"

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
    # generate a UUID
    user.id = uuid.uuid4()
    # hash the password before saving to the database
    user.password = pbkdf2_sha256.hash(user.password)
    users.append(user)
    db.writeUsrData(users)
    return dict(user)

@router.get("/api/users", tags=["get"])
async def all_users(request: Request) -> dict:
    """
    Returns all the users. No parameter needed.

    Example with curl:
        curl -H "Content-type: application/json" -H "Accept: application/json" -i -L  http://localhost:8000/api/users

    :return: All the elements
    """
    users = db.readUsrData()
    return {"message": "Users database", "method": request.method, "users": users}

@router.get("/api/user/email", status_code=status.HTTP_200_OK, tags=["content_parameter"])
async def user_email(userEmail: Email) -> dict:
    """
    This API returns all the information of a user given its email address.

    Example with curl:
        curl -X GET -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"email": "user3@example.com"}' -i -L "http://localhost:8000/api/user/email"
    :param userEmail: The email address of the user we want to retreive
    :return: The user or error 404 if not found
    """
    users = db.readUsrData()
    record = [d for d in users if d.email == userEmail.email]
    if record:
        # record is a list with only one element, if email is unique 😉
        return {"user": record[0]}

    strError = f"User with email {userEmail.email} was not found"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strError,
        headers={"X-Fake-REST-API": strError},
    )

@router.get("/api/user/validate", status_code=status.HTTP_200_OK, tags=["content_parameter"])
async def user_validation(userCredential: EmailPassword) -> dict:
    """
    This API returns:
        200 if the user exists and the password is valid
        401 if password is invalid
        404 if email doesn't exist

    Example with curl:
        curl -X GET -H "Content-type: application/json" -H "Accept: application/json" \
        -d '{"email": "user6@example.com", "password": "Password6"}' -i -L "http://localhost:8000/api/user/validate"
    :param userCredential: The email address of the user we want to retreive
    :return: See above
    """
    users = db.readUsrData()
    record = [d for d in users if d.email == userCredential.email]
    if record:
        print(record[0])
        # record is a list with only one element, if email is unique 😉
        try:
            verification = pbkdf2_sha256.verify(userCredential.password, record[0].password)
            if verification:
                return {"credential": verification}
            else:
                strError = f"Invalid email address or password"
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=strError,
                    headers={"X-Fake-REST-API": strError},
                )
        except ValueError:
            return {"error": "Internal database error. Is the password hashed?"}

    strError = f"User with email {userCredential.email} was not found"
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
