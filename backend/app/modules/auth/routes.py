from fastapi import APIRouter, Response, Depends
from app.modules.auth.schemas import RegisterSchema, LoginSchema
from app.modules.auth.service import register_user, login_user, logout_user
from app.core.dependencies import get_current_user

router = APIRouter()

# -------------------------
# REGISTER
# -------------------------
@router.post("/register")
def register(data: RegisterSchema):
    return register_user(data)


# -------------------------
# LOGIN
# -------------------------
@router.post("/login")
def login(data: LoginSchema, response: Response):
    """
    Login user and store JWT in HTTPOnly cookie
    """
    return login_user(data, response)


# -------------------------
# LOGOUT
# -------------------------
@router.post("/logout")
def logout(response: Response):
    """
    Remove authentication cookie
    """
    return logout_user(response)


# -------------------------
# CURRENT USER
# -------------------------
@router.get("/me")
def get_me(user=Depends(get_current_user)):
    """
    Get current logged in user
    """
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"]
    }