
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from token_utils import verify_token


security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(token.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload


def admin_required(token: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(token.credentials)
    if payload is None or payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can access this route")
    return payload
