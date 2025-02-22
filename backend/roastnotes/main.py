from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from roastnotes.core.config import settings
from loguru import logger

from roastnotes.router import users, groups, roasts, roasters, ratings

app = FastAPI()
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(roasts.router)
app.include_router(roasters.router)
app.include_router(ratings.router)

if settings.ENVIRONMENT == "dev":
    logger.info("Running in development mode - CORS enabled for development origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Local development
            "http://localhost:5173",  # Vite default port
            # "https://stash-peach.vercel.app"  # Production deployment
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "accept"],
        expose_headers=["*"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )
else:
    logger.info("Running in production mode - CORS enabled for production origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            # "https://stash-peach.vercel.app",  # Production deployment
            "http://localhost:5173",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "accept"],
        expose_headers=["*"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}
