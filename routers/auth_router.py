from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine
from models import User
from schemas import UserRegister, UserLogin, TokenResponse, TokenPayload
from auth_utils import get_db, create_access_token, verify_token
from crud import create_user, authenticate_user

Base.metadata.create_all(bind=engine)
router = APIRouter()

@router.post("/register", response_model=dict)
def register(body: UserRegister, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == body.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, name=body.name, email=body.email, password=body.password)
    return {"id": user.id, "name": user.name, "email": user.email}

@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=user.email, name=user.name)
    return TokenResponse(access_token=token)

@router.get("/verify-token", response_model=TokenPayload)
def verify(payload: dict = Depends(verify_token)):
    return TokenPayload(sub=payload["sub"], name=payload["name"], exp=payload["exp"])
