from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserSignup, UserLogin
from app.utils.security import verify_password
from fastapi import Header
from app.utils.security import verify_token

from app.schemas.user_schema import UserSignup
from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password
from app.utils.security import (
    verify_password,
    create_access_token
)

router = APIRouter()
@router.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already exists"
        }

    hashed_pw = hash_password(
        user.password
    )

    new_user = User(
        email=user.email,
        password_hash=hashed_pw
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "email": new_user.email
    }
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "Invalid email or password"
        }

    valid_password = verify_password(
        user.password,
        db_user.password_hash
    )

    if not valid_password:
        return {
            "message": "Invalid email or password"
        }

    access_token = create_access_token(
    {
        "sub": db_user.email
    }
)

    return {
    "access_token": access_token,
    "token_type": "bearer"
}

@router.get("/test")
def test():
    return {
        "message": "Auth routes working"
    }

@router.get("/profile")
def profile(token: str):

    email = verify_token(token)

    if not email:
        return {
            "message": "Invalid token"
        }

    return {
        "message": "Protected route accessed",
        "email": email
    }