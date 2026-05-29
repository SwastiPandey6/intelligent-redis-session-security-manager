from fastapi import APIRouter
from app.schemas.user_schema import UserSignup
from app.utils.security import hash_password

router = APIRouter()

fake_users_db = []

@router.post("/signup")
def signup(user: UserSignup):

    hashed_pw = hash_password(user.password)

    fake_users_db.append({
        "email": user.email,
        "password": hashed_pw
    })

    return {
        "message": "User registered successfully",
        "user": user.email
    }
@router.post("/login")
def login(user: UserSignup):

    for db_user in fake_users_db:

        if db_user["email"] == user.email:

            return {
                "message": "Login successful"
            }

    return {
        "message": "Invalid credentials"
    }