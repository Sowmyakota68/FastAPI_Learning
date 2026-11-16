#Database connection setup cheyyali	---->  database.py
#Database table structure define cheyyali ----> 	models.py
#GET, POST, PUT, DELETE APIs create cheyyali ----> 	main.py
#Database nunchi data retrieve cheyyali ----> 	main.py lo endpoint + database session
#Kotha column add cheyyali----> 	models.py — tarvata database migration/update avasaram
#Database file create/use cheyyali ----> 	database.py lo URL configure cheyyali

#database.py — Database connection
#models.py — Table structure
#main.py — Database session tho GET, POST operations
#schemas.py — Pydantic validation
#crud.py — Database operations ni separate cheyyadam
#routers/ — APIs ni organize cheyyadam
"""
FastAPI Application
                |
                |
        Database Connection
                |
                |
       Create Database Tables
                |
                |
        Client sends GET request
                |
                |
          FastAPI receives it
                |
                |
        get_db() is executed
                |
                |
       Database Session Created
                |
                |
       Query executes on Todos table
                |
                |
        Fetch all Todo records
                |
                |
          Return Response
                |
                |
        Close Database Session
"""
from fastapi import FastAPI
app = FastAPI()
from .Database import engine
from .model import Base
from .routers import auth,todos,admin,users

Base.metadata.create_all(bind=engine) 
#Idi defined models prakaram database lo tables create chestundi.
#Base.metadata.create_all(bind=engine)	-----> Defined models kosam tables create chestundi, table lenappudu

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
#include_router() = ఆ separate files లో ఉన్న APIs ని main application కి connect చేయడానికి.

@app.get("/healthy")
def health_check():
    return {"status": "healthy"}


