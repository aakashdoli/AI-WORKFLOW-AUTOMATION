from fastapi import FastAPI
from backend.api.v1.workflows import router as workflow_router
from backend.services.database_service import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Ops Platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
@app.on_event("startup")
def startup():
    init_db()

# Routers
app.include_router(workflow_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai-ops-api"}
