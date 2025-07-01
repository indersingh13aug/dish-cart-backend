from app.core.gemini_client import gemini_chat
import random
import json,re
import requests

def handle_recipe(query: str) -> str:
    prompt = f"""
                You are a polite and helpful cooking assistant. The user wants a recipe for:

                Give me a recipe for {query}

                Rules:
                - Only provide recipes that actually exist and are commonly known or plausible.
                - If the requested recipe does not exist, or is outside your knowledge, reply politely with this JSON instead:
                - Do NOT make up ingredients or instructions you are unsure about.
                - Keep instructions concise, maximum 15 steps.
                - Only include up to 20 ingredients.
                - Provide your reply as pure JSON:
                    - recipe_name: string or null
                    - instructions: list of strings (each step separately).
                    - ingredients: list of objects:
                        - name: string
                        - quantity: string (e.g. "100 grams", "50 ml", etc.)
                - DO NOT wrap the JSON in triple backticks.
                - DO NOT add any extra text or explanation.
                - Only return pure JSON.
    """

# - quantity: string (e.g. "100 grams", "50 ml", etc.)
    raw = gemini_chat(prompt)
    print(raw)
    # Remove triple backticks if present
    cleaned = re.sub(r"^```(?:json)?\n", "", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\n```$", "", cleaned.strip(), flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "").strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # fallback
        return json.dumps({
            "recipe_name": "Unknown Recipe",
            "ingredients": [],
            "instructions":[]
        })

    recipe_name = data.get("recipe_name", "Unknown Recipe")
    instructions = data.get("instructions", [])
    ingredients = data.get("ingredients", [])
    print('ingredients',ingredients)
    # new_ingredients = []
    # if ingredients:
    #     for ing in data["ingredients"]:
    #         name = ing["name"]
    #         new_ingredients.append({
    #             "name": name,
    #         })


    # ✅ RETURN JSON instead of HTML
    return json.dumps({
        "recipe_name": recipe_name,
        "instructions": instructions,
        "ingredients": ingredients,
    })



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


# def fetch_unsplash_image(query):
#     url = f"https://api.unsplash.com/search/photos"
#     params = {
#         "query": query,
#         "client_id": "Y9L61AQWXaGUTBhAdqtM_MhdYqvHYGeia64X2ReFex4",
#         "per_page": 1
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     return data["results"][0]["urls"]["regular"]