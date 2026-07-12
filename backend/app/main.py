from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import auth, dashboard, environmental, social, governance, gamification, reports, ai, settings

import app.models.user
import app.models.department
import app.models.settings
import app.models.notification
import app.models.esg_score
import app.models.environmental
import app.models.social
import app.models.governance
import app.models.gamification

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoSphere API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(environmental.router)
app.include_router(social.router)
app.include_router(governance.router)
app.include_router(gamification.router)
app.include_router(reports.router)
app.include_router(ai.router)
app.include_router(settings.router)


@app.get("/")
def root():
    return {"status": "ok", "app": "EcoSphere", "docs": "/docs"}
