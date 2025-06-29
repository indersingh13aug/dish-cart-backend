from app.services import (
    recipe_service,
    cart_service,
    classification_service,
)
from app.core.gemini_client import gemini_chat
from app.models.schemas import ChatResponse

def orchestrate(user_id: str, user_message: str) -> ChatResponse:
    intent = classification_service.classify_intent(user_message)
    print(f"[DEBUG] Final classified intent: {intent}")

    if intent == "recipe_request":
        response = recipe_service.handle_recipe(user_message)
    elif intent == "ingredient_query":
        response = recipe_service.product_listing(user_message)
    elif intent == "add_to_cart":
        response = cart_service.add_to_cart(user_id, user_message)
    elif intent == "view_cart":
        response = cart_service.view_cart(user_id)
    elif intent == "remove_from_cart":
        response = cart_service.remove_from_cart(user_id, user_message)
    elif intent == "checkout":
        response = cart_service.checkout(user_id)
    elif intent == "clear_cart":
        response = cart_service.clear_cart(user_id)
    else:
        response = gemini_chat(
            f"You are a helpful cooking assistant. User said: {user_message}\n Reply politely."
        )

    return ChatResponse(
        assistant_message=response,
        intent=intent,
    )
