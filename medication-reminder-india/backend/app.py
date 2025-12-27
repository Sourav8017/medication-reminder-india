from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.auth import router as auth_router
from backend.routes.users import router as users_router
from backend.routes.medications import router as medications_router
from backend.routes.reminders import router as reminders_router

app = FastAPI(
    title="Indian Medication Reminder & Health Risk Predictor",
    description="India-first healthcare AI with reminders and ML hooks",
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
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"health": "UP"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(medications_router)
app.include_router(reminders_router)
