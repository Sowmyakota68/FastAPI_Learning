"""
db.commit()-----> 	Database transaction changes commit chestundi


"""
from sqlalchemy import create_engine #create_engine() -----> Database engine setup
from sqlalchemy.orm import sessionmaker #sessionmaker() -----> Database sessions create cheyadaniki factory
from sqlalchemy.ext.declarative import declarative_base #declarative_base()-----> 	Models ki foundation

SQLALCHEMY_DATABASE_URL ="postgresql+psycopg2://postgres:Nagamani%4018@localhost:5432/todo_application_database"  #SQLALCHEMY_DATABASE_URL -----> 	Database ekkada undo cheptundi

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False,bind=engine) #SessionLocal()	-----> Oka database session create chestundi

Base = declarative_base() 
#declarative_base()-----> Models ki foundation 
#SQLAlchemy database models create cheyadaniki oka base class ni create chestundi. 
# Model = Database table ki blueprint (design).
#Model ante database table ela undalo define chese Python class.

