from app.core.gemini_client import gemini_chat

VALID_INTENTS = {
    "recipe_request",
    "ingredient_query",
    "add_to_cart",
    "view_cart",
    "remove_from_cart",
    "checkout",
    "clear_cart",
}

def classify_intent(message: str) -> str:
    prompt = f"""
    Classify this user message into one of:
    - recipe_request
    - ingredient_query
    - add_to_cart
    - view_cart
    - remove_from_cart
    - checkout
    - clear_cart

    ONLY return the keyword, nothing else.

    User message: {message}
    """
    predicted_intent = gemini_chat(prompt).strip().lower()
    if predicted_intent in VALID_INTENTS:
        return predicted_intent
    
    # fallback if hallucination
    return "general_query"
