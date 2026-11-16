from fastapi import HTTPException,Depends,Path,APIRouter
from ..Database import SessionLocal
from ..model import Todos
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user

router = APIRouter()
user_dependency = Annotated[dict, Depends(get_current_user)]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    Description:str = Field(min_length=3,max_length=100)
    Priority:int
    Complete:bool

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/")
def read_all(user:user_dependency,db:db_dependency):
    if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                    detail="Could not validate credentials")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
def get_id(user:user_dependency,db:db_dependency,todo_id:int =Path(gt = 0)):
    if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate credentials")
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="Todo not found")

@router.post("/todo",status_code=status.HTTP_200_OK)
def post_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                detail="Could not validate credentials")
    todo_model = Todos(**todo_request.dict(),owner_id = user.get("id"))


    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}",status_code=status.HTTP_200_OK)
def update_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest,
                todo_id:int =Path(gt = 0)):
    if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
       raise HTTPException(status_code=404,detail="Todo not found") 

    todo_model.title = todo_request.title
    todo_model.Description = todo_request.Description
    todo_model.Priority = todo_request.Priority
    todo_model.Complete = todo_request.Complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}",status_code=status.HTTP_200_OK)
def delete_todo(user:user_dependency,db:db_dependency,todo_id:int =Path(gt = 0)):
    if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate credentials")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    if todo_model is None:
       raise HTTPException(status_code=404,detail="Todo not found") 
    db.delete(todo_model)
    db.commit()
    raise HTTPException(status_code=200, detail="todo deleted success")
    