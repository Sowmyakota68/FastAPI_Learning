from fastapi import APIRouter,Depends,HTTPException,status
#APIRouter() = APIs ని separate files లో organize చేయడానికి.
from pydantic import BaseModel,Field
from ..model import Users
from passlib.context import CryptContext
from ..Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta,datetime
router = APIRouter(
    prefix = "/auth",
    tags= ["auth"]

)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "b554e9d4e17d88ea85e2504b6f36cb312a6693c16cdcc96cc059282350dfd0cb"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    email : str
    username : str
    first_name :str
    last_name:str
    password: str
    is_active :bool
    role:str

class ChangePasswordRequest(BaseModel):
    old_password:str
    new_password:str


def authenticate_user(username : str, password:str,db):
    auth_user = db.query(Users).filter(Users.username == username).first()
    if not auth_user:
        return False
    if not bcrypt_context.verify(password,auth_user.hased_password):
        return False
    return auth_user

def create_access_token(username : str, user_id:int, role:str, expires_delta : timedelta):
    encode = {"sub": username, "id": user_id, "role" : role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        print("TOKEN RECEIVED:", token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        user_id : int = payload.get("id")
        role : str = payload.get("role")
        print("PAYLOAD:", payload)

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
        return {
        "username": username,
        "id": user_id,
        "role":role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not validate credentials")

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/")
def create_user(db:db_dependency, createuserrequest: CreateUserRequest):
    create_user_model = Users(
        email = createuserrequest.email,
        username = createuserrequest.username,
        first_name = createuserrequest.first_name,
        last_name = createuserrequest.last_name,
        hased_password = bcrypt_context.hash(createuserrequest.password),
        is_active = createuserrequest.is_active,
        role = createuserrequest.role
    )
    
    db.add(create_user_model)
    db.commit()

@router.get("/authusers") 
def get_users(db:db_dependency):
    return db.query(Users).all()  


@router.post("/token")
def vetify_details(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    token = create_access_token(user.username,user.id,user.role, timedelta(minutes=20))
    return {
    "access_token": token,
    "token_type": "bearer"
}
    
@router.put("/changePassword")
def change_Password(user:user_dependency,db:db_dependency,changepasswordmodel:ChangePasswordRequest):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Could not validate credentials")

    if not bcrypt_context.verify(changepasswordmodel.old_password , user_model.hased_password):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="Could not validate credentials")

    user_model.hased_password = bcrypt_context.hash(changepasswordmodel.new_password)
    db.commit()

    return {"message": "Password changed successfully"}

    