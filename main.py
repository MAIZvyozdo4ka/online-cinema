from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas import UserCreate
from crud import get_user_by_username, create_user
from auth import verify_password

#в бд другой пользователь

app = FastAPI()

@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)

@app.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful"}

#сделать ошибки по ооп