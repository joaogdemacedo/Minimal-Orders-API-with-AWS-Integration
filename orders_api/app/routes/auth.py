from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from auth.jwt_handler import create_access_token
import logging

router = APIRouter(tags=["Auth"])
logger = logging.getLogger(__name__)

# Mocked user (normally you'd check a DB)
fake_user = {
    "username": "string",
    "password": "string",
    "user_id": "user-123"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    logger.info(f"POST /login attempt for username: {data.username}")
    if data.username != fake_user["username"] or data.password != fake_user["password"]:
        logger.warning(f"Failed login attempt for username: {data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token({"sub": fake_user["user_id"]})
    logger.info(f"Login success for user_id: {fake_user['user_id']}")
    return {"access_token": token, "token_type": "access_token"}