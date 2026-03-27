from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.modules.auth.routes import router as auth_router
from app.modules.crop_recommendation.routes import router as crop_router
from app.modules.fertilizer.routes import router as ferti_router
from app.modules.chatbot.routes import router as chatbot_router  # <-- New chatbot router
from app.modules.agreements.agreement_routes import router as agreement_router

from app.core.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Agri Assistant API")

# ---------------- Startup / Shutdown ----------------
@app.on_event("startup")
def startup():
    connect_to_mongo()

@app.on_event("shutdown")
def shutdown():
    close_mongo_connection()

# ---------------- Include Routers ----------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(crop_router, prefix="/crop", tags=["Crop Recommendation"])
app.include_router(ferti_router, prefix="/fertilizer", tags=["Fertilizer Recommendation"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])  # <-- Chatbot router
app.include_router(agreement_router, prefix="/agreement", tags=["Agreement"])

# ---------------- Serve Static Audio Files ----------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")