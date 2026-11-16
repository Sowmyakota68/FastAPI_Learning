from fastapi import APIRouter,Depends,HTTPException,Path
from .auth import get_current_user
from typing import Annotated
from ..Database import SessionLocal
from sqlalchemy.orm import Session
from ..model import Todos

router = APIRouter(
    prefix = "/admin",
    tags = ["admin"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]



@router.get("/todo")
def get_admin_todo(user:user_dependency,db:db_dependency):
    
    if user is None or user.get("role") != "admin":
        raise HTTPException(
        status_code=401,
        detail="Authentication Failed"
    )
    return db.query(Todos).all()


@router.delete("/deletetodo/{todo_id}")
def delete_todo_by_admin(user:user_dependency,db:db_dependency,todo_id:int =Path(gt = 0)):
    if user is None or user.get("role") != "admin":
             raise HTTPException(
                status_code=401,
                detail="Authentication Failed"
            )
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
         raise HTTPException(
                 status_code=401,
                 detail="Authentication Failed"
             )
    db.delete(todo_model)
    db.commit()