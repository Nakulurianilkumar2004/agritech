from fastapi import HTTPException, Response
from app.modules.auth.repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token


# -------------------------
# REGISTER
# -------------------------
def register_user(data):
    existing = get_user_by_email(data.email)

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "email": data.email,
        "password": hash_password(data.password),
        "role": "user"
    }

    result = create_user(user_data)  # ✅ MongoDB result object

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)  # ✅ FIXED (important)
    }


# -------------------------
# LOGIN
# -------------------------
def login_user(data, response: Response):

    user = get_user_by_email(data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "sub": str(user["_id"]),
        "role": user["role"]
    })

    # Set JWT cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "Login successful",
        "role": user["role"]
    }


# -------------------------
# LOGOUT
# -------------------------
def logout_user(response: Response):

    response.delete_cookie("access_token")

    return {
        "message": "Logged out successfully"
    }