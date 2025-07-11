from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, engine_a, engine_b
from app import models
from app.routers import contribuinte
from app.config import settings

# Create database tables for all databases
models.Base.metadata.create_all(bind=engine)  # Legacy database
models.Base.metadata.create_all(bind=engine_a)  # Module A database
models.Base.metadata.create_all(bind=engine_b)  # Module B database

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(contribuinte.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cursor Easy Backend",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 