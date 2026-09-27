from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.config import get_settings

from backend.routes import router


settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    description=(
        "AI-powered legal document "
        "drafting and export API."
    ),

    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================
# ROUTES
# ==========================================

app.include_router(
    router
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():

    return {

        "message":
            "LegalEase API is running.",

        "docs":
            "/docs",

        "health":
            "/health"
    }