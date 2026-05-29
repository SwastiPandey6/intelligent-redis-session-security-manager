from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.database import Base, engine
from app.models.user import User

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Backend Running Successfully"}