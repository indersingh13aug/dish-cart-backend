from app.core.gemini_client import gemini_chat
import random
import json,re
import requests

def fetch_unsplash_image(query):
    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": "Y9L61AQWXaGUTBhAdqtM_MhdYqvHYGeia64X2ReFex4",
        "per_page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["results"][0]["urls"]["regular"]

def handle_recipe(query: str) -> str:
    prompt = f"""
    You are a cooking assistant. User wants a recipe for:

    {query}

    Provide your reply as JSON with fields:
    - recipe_name: string
    - ingredients: list of objects:
        - name: string
        - Only return image_url values from real, publicly available royalty-free images that are currently accessible (no 404).
        - If unsure, use generic placeholder images like https://via.placeholder.com/150

    - instructions: optional string
    Important:
        - DO NOT wrap the JSON in triple backticks.
        - DO NOT add any extra text or explanation.
        - Only return pure JSON.
    """

    raw = gemini_chat(prompt)

    # Clean triple backticks if present
    cleaned = re.sub(r"^```(?:json)?\n", "", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\n```$", "", cleaned.strip(), flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "").strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return raw

    recipe_name = data.get("recipe_name", "Unknown Recipe")
    ingredients = data.get("ingredients", [])
    ingredients = []
    for ing in data["ingredients"]:
        name = ing["name"]
        image_url = fetch_unsplash_image(name)
        ingredients.append({
            "name": name,
            "image_url": image_url,
        })

    instructions = data.get("instructions", "")

    html = f"""
    <h3 style="color:#D2691E;">🍽️ {recipe_name}</h3>
    <h4>Ingredients:</h4>
    <div style="display: flex; flex-wrap: wrap; gap: 16px;">
    """
    for ing in ingredients:
        name = ing.get("name", "")
        image_url = ing.get("image_url", "")
        html += f"""
            <div style="width: 150px; text-align: center;">
                <img src="{image_url}" alt="{name}" style="width: 100%; height: auto; border-radius: 8px;" />
                <p>{name}</p>
            </div>
        """

    html += "</div>"


    if instructions:
        # split numbered instructions to separate lines
        steps = re.findall(r"\d+\.\s.*?(?=\s\d+\.|$)", instructions.strip(), re.DOTALL)
        html += "<h4>Instructions:</h4><ol>"
        for step in steps:
            # Remove the leading "1. " etc.
            text = re.sub(r"^\d+\.\s*", "", step.strip())
            html += f"<li>{text}</li>"
        html += "</ol>"

    return html

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
