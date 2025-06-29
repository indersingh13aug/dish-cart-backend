from app.utils.session_manager import SESSIONS, save_sessions
import random

def add_to_cart(user_id: str, query: str) -> str:
    item = {
        "name": query,
        "price": random.randint(80, 150)
    }
    SESSIONS.setdefault(user_id, []).append(item)
    save_sessions()
    return (
        f"✅ Added **{query}** (₹{item['price']}) to your cart.\n\n"
        f"Would you like to view your cart, remove something, or checkout?"
    )

def view_cart(user_id: str) -> str:
    cart = SESSIONS.get(user_id, [])
    if not cart:
        return "🛒 Your cart is empty."

    msg = "🛒 **Your Cart:**\n"
    total = 0
    for i, item in enumerate(cart, 1):
        msg += f"{i}. {item['name']} – ₹{item['price']}\n"
        total += item["price"]

    msg += f"\n**Total:** ₹{total}\n"
    msg += "Would you like to remove an item or checkout?"
    return msg

def remove_from_cart(user_id: str, query: str) -> str:
    cart = SESSIONS.get(user_id, [])
    for i, item in enumerate(cart):
        if query.lower() in item["name"].lower():
            removed_item = cart.pop(i)
            save_sessions()
            return f"✅ Removed **{removed_item['name']}** from your cart."
    return f"⚠️ Could not find **{query}** in your cart."

def checkout(user_id: str) -> str:
    cart = SESSIONS.get(user_id, [])
    if not cart:
        return "Your cart is empty. Add something before checkout!"

    total = sum(item["price"] for item in cart)
    SESSIONS[user_id] = []
    save_sessions()
    return f"✅ Order placed! Total amount: ₹{total}. Thank you for shopping!"

def clear_cart(user_id: str) -> str:
    SESSIONS[user_id] = []
    save_sessions()
    return "🗑️ Your cart has been cleared."
