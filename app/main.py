from fastapi import FastAPI
from app.api.v1.endpoints import chat, recipes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="DishCart AI Backend"
    ,docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "https://dish-kart.netlify.app/",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(recipes.router, prefix="/api", tags=["recipes"])
