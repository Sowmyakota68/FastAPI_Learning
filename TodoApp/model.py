# Model = Database table ki blueprint (design).
#Model ante database table ela undalo define chese Python class.
#class Todo(Base)	-----> Table structure define chestundi
from .Database import Base
from sqlalchemy import Column, Integer,String, Boolean,ForeignKey


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    Description = Column(String)
    Priority = Column(Integer)
    Complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hased_password = Column(String)
    is_active = Column(Boolean,default= True)
    role = Column(String)
    phone_number = Column(String, nullable=False)

