from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import init_db
from .routes.health import router as health_router
from .routes.describe import router as describe_router
from .routes.input_tokens import router as input_tokens_router

app = FastAPI(title="Image Describer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(health_router)
app.include_router(describe_router)
app.include_router(input_tokens_router)
