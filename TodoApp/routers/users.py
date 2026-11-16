from fastapi import APIRouter,Depends,HTTPException
from .auth import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from ..Database import SessionLocal
from ..model import Users
from pydantic import BaseModel

router = APIRouter(
    prefix = "/Users",
    tags=["Users"]
)
# create database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]

class UpdatePhoneNumberModel(BaseModel):
     phone_number:str

@router.get("/")
def get_active_users(user:user_dependency,db:db_dependency):
    user_model = db.query(Users).filter(user.get('id')== Users.id).first()
    if user_model is None:
        raise HTTPException(
                        status_code=401,
                        detail="Authentication Failed"
                    )    
    return user_model
# update phone number
@router.put("/update_phone")
def update_user_phone_number(user:user_dependency,db:db_dependency,updateNumber:UpdatePhoneNumberModel):
     user_model = db.query(Users).filter(user.get('id')== Users.id).first()
     if user_model is None:
             raise HTTPException(
                             status_code=401,
                             detail="Authentication Failed"
                         )    
     user_model.phone_number = updateNumber.phone_number
     db.commit()
     return("phone number update sucess")