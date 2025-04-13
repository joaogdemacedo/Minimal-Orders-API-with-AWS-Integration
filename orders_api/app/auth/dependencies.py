from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from auth.jwt_handler import verify_access_token
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

def get_current_user(authorization: str = Depends(security)):
    logger.info(f"Incoming auth header")
    if not authorization or not authorization.credentials:
        logger.warning("Missing or invalid token")
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.credentials
    payload = verify_access_token(token)
    logger.info(f"Decoded token payload")
    
    if not payload:
        logger.warning("Invalid or expired token")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["sub"]