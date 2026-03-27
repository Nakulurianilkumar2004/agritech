from fastapi import Depends, HTTPException, Request, status
from app.core.security import decode_token
from app.modules.auth.repository import get_user_by_id

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        # Admin can access everything
        if user["role"] != required_role and user["role"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return user
    return role_checker