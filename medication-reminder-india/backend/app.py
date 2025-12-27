from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth import router as auth_router
from backend.routes.users import router as users_router

app = FastAPI(
    title="Indian Medication Reminder & Health Risk Predictor",
    description="India-first healthcare AI system using NLEM medicines and synthetic patient data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Indian Medication Reminder Backend Running",
        "status": "OK"
    }

@app.get("/health")
def health_check():
    return {"health": "UP"}

# Routers
app.include_router(auth_router)
app.include_router(users_router)
