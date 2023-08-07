from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependecy):
    """
    Read all todos.

    Args:
        db (db_dependecy): The database dependency to be injected

    Returns:
        todos: The list of todos
    """
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependecy, todo_id: int = Path(gt=0)):
    """
    Read todo by ID.

    Args:
        db (db_dependecy): The database dependency to be injected
        todo_id (int): ID of the todo

    Raises:
        HTTPException: Request todo ID is not found

    Returns:
        todo: Todo matching the ID
    """
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependecy, todo_request: TodoRequest):
    """
    Add a new todo.

    Args:
        db (db_dependecy): The database dependency to be injected
        todo_request (TodoRequest): Request to add a todo
    """
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependecy, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    """
    Update a todo.

    Args:
        db (db_dependecy): The database dependency to be injected
        todo_id (int): ID of the todo to be updated
        todo_request (TodoRequest): Request to update a todo

    Raises:
        HTTPException: Request todo ID is not found
    """
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependecy, todo_id: int = Path(gt=0)):
    """
    Delete a todo.

    Args:
        db (db_dependecy): The database dependency to be injected
        todo_id (int): ID of todo to be deleted

    Raises:
        HTTPException: Request todo ID is not found
    """
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
