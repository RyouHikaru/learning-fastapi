from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Users
from database import SessionLocal
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "ef8881a99f357123d5d394aceb83c46697a261e899a5cef0d83b5132920c3ecd"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    """
    Authenticate user.

    Args:
        username (str): Username
        password (str): Password
        db (db_dependency): The db dependency to be injected

    Returns:
        user: The user or False if authentication fails
    """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    """
    Generate access token.

    Args:
        username (str): Username
        user_id (int): User ID
        role (str): Role of user
        expires_delta (timedelta): Expiration time of token

    Returns:
        jwt: The generated JWT
    """
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Get current user from token.

    Args:
        token (Annotated[str, Depends): JWT

    Raises:
        HTTPException: The username or user is invalid or JWT is invalid

    Returns:
        user: The details of the currently logged in user
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependecy, create_user_request: CreateUserRequest):
    """
    Add a user.

    Args:
        db (db_dependecy): The db dependency to be injected
        create_user_request (CreateUserRequest): Request for adding a user
    """
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependecy):
    """
    User login.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): The form data dependency to be injected
        db (db_dependecy): The db dependency to be injected

    Raises:
        HTTPException: The user is not found

    Returns:
        jwt: The generated JWT
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
