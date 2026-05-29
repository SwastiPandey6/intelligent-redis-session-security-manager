from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserSignup
from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password

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

@router.get("/test")
def test():
    return {
        "message": "Auth routes working"
    }