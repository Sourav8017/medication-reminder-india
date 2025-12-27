from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "CHANGE_THIS_TO_ENV_LATER"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register_user(
    name: str,
    age: int,
    phone: str,
    password: str,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.phone == phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Phone already registered")

    user = User(
        name=name,
        age=age,
        phone=phone,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(phone: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.phone})
    return {"access_token": token, "token_type": "bearer"}
