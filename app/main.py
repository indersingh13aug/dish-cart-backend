from fastapi import FastAPI
from app.api.v1.endpoints import chat, recipes

app = FastAPI(title="DishCart AI Backend")

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["recipes"])
