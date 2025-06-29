from app.core.gemini_client import gemini_chat
import random

def handle_recipe(query: str) -> str:
    prompt = f"""
    You are a cooking assistant. User wants a recipe for:

    {query}

    Provide:
    - Confirmed recipe name
    - Bullet list of ingredients with quantities
    """
    return gemini_chat(prompt)

def product_listing(query: str) -> str:
    products = []
    for _ in range(3):
        brand = random.choice(["India Gate", "Daawat", "Organic Choice"])
        quantity = "1kg"
        price = random.randint(80, 150)
        store = random.choice(["JioMart", "Amazon", "Flipkart"])
        link = "http://example.com/product"

        products.append({
            "ingredient": query,
            "brand": brand,
            "quantity": quantity,
            "price": price,
            "store": store,
            "link": link,
        })

    product_list_str = f"Here are some options for **{query}**:\n\n"
    for p in products:
        product_list_str += (
            f"✅ {p['brand']} {p['ingredient']} {p['quantity']} "
            f"– ₹{p['price']} – {p['store']} – [Link]({p['link']})\n"
        )
    return product_list_str
