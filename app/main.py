from fastapi import FastAPI
from app.api.v1.endpoints import chat, recipes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="DishCart AI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["recipes"])
