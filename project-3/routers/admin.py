from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy, db: db_dependecy):
    """
    Read all todos.

    Args:
        user (user_dependecy): The user dependency to be injected
        db (db_dependecy): The db dependency to be injected

    Raises:
        HTTPException: The user is not an admin

    Returns:
        _type_: All todos
    """
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy, db: db_dependecy, todo_id: int = Path(gt=0)):
    """
    Delete a todo.

    Args:
        user (user_dependecy): The user dependency to be injected
        db (db_dependecy): The db dependency to be injected
        todo_id (int): ID of todo to be deleted

    Raises:
        HTTPException: The user is not an admin or todo ID is not found
    """
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
