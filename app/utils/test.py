# from serpapi import GoogleSearch

# api_key = "0b307be8fba597f102860a9eba12f10d7a6d643283cc1efc8813299ca9f3923e"


# search = GoogleSearch({
#     "q": "site:flipkart.com basmati rice 1kg",
#     "api_key": api_key
# })

# results = search.get_dict()
# results = {
#     "organic_results" :[{
#     "position": 1,
#     "title": "India Gate Basmati Rice/Basmati Akki - Classic 1 kg",
#     "link": "https: //www.bigbasket.com/pd/243336/india-gate-basmati-rice-classic-1-kg-pouch/",
#     "redirect_link": "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.bigbasket.com/pd/243336/india-gate-basmati-rice-classic-1-kg-pouch/&ved=2ahUKEwjAso2Tn52OAxWN8rsIHcFvI5MQFnoECBoQAQ",
#     "displayed_link": "https://www.bigbasket.com › ... › basmati rice",
#     "favicon": "https://serpapi.com/searches/6864a8e8532a17e19c15ccf6/images/92f2ef0c5f6396b5dd1c2a46a9a31dc8f6e831e88e293ef3a76b275ee9970b3c.png",
#     "snippet": "India Gate Basmati Rice/Basmati Akki - Classic, 1 kg · 1 kg. Rs 231.25. MRP: Rs 252. 5 mins. ₹21 OFF · 5 kg. Rs 1142. Bag. MRP: Rs 1170. 5 mins. ₹28 OFF ...",
#     "snippet_highlighted_words": [
#         "India Gate Basmati Rice/Basmati Akki - Classic, 1 kg"
#     ],
#     "rich_snippet": {
#         "bottom": {
#             "detected_extensions": {
#                 "price": 231.25,
#                 "currency": "₹",
#                 "rating": 4.2,
#                 "reviews": 3460
#             },
#             "extensions": [
#                 "₹231.25",
#                 "In stock",
#                 "4.2(3,460)",
#                 "7-day returns"
#             ]
#         }
#     },
#     "source": "BigBasket"
# }]
# }

# for r in results.get("organic_results", []):
#     print(r)
#     print(r["title"])
#     print(r["rich_snippet"]["bottom"]["extensions"][0])
#     print(r["favicon"])

import re

# your JSON list
results = [
   {
    "position": 1,
    "title": "India Gate Basmati Rice/Basmati Akki - Classic 1 kg",
    "link": "https: //www.bigbasket.com/pd/243336/india-gate-basmati-rice-classic-1-kg-pouch/",
    "redirect_link": "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.bigbasket.com/pd/243336/india-gate-basmati-rice-classic-1-kg-pouch/&ved=2ahUKEwjAso2Tn52OAxWN8rsIHcFvI5MQFnoECBoQAQ",
    "displayed_link": "https://www.bigbasket.com › ... › basmati rice",
    "favicon": "https://serpapi.com/searches/6864a8e8532a17e19c15ccf6/images/92f2ef0c5f6396b5dd1c2a46a9a31dc8f6e831e88e293ef3a76b275ee9970b3c.png",
    "snippet": "India Gate Basmati Rice/Basmati Akki - Classic, 1 kg · 1 kg. Rs 231.25. MRP: Rs 252. 5 mins. ₹21 OFF · 5 kg. Rs 1142. Bag. MRP: Rs 1170. 5 mins. ₹28 OFF ...",
    "snippet_highlighted_words": [
        "India Gate Basmati Rice/Basmati Akki - Classic, 1 kg"
    ],
    "rich_snippet": {
        "bottom": {
            "detected_extensions": {
                "price": 231.25,
                "currency": "₹",
                "rating": 4.2,
                "reviews": 3460
            },
            "extensions": [
                "₹231.25",
                "In stock",
                "4.2(3,460)",
                "7-day returns"
            ]
        }
    },
    "source": "BigBasket"
},
{
    "position": 1,
    "title": "INDIA GATE CLASSIC Basmati Rice (Long Grain ...",
    "link": "https://www.flipkart.com/india-gate-classic-basmati-rice-long-grain/p/itmex3vw9tveyzrr",
    "redirect_link": "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.flipkart.com/india-gate-classic-basmati-rice-long-grain/p/itmex3vw9tveyzrr&ved=2ahUKEwiYiKnioZ2OAxV2rZUCHfVRHRQQFnoECBoQAQ",
    "displayed_link": "https://www.flipkart.com › india-gate-classic-basmati-ri...",
    "favicon": "https://serpapi.com/searches/6864aba83b93e353e2f509e6/images/3d422b327a42bb751525760420798b6408d162069847337f620454f465e51797.png",
    "snippet": "CLASSIC Basmati Rice (Long Grain, Unpolished) (1 kg). 4.0. •. Good • 4 ratings. 27%. ₹399. ₹290. @ ₹290/kg. Hurry, Only a few left! Quantity: 1 kg. 1 kg.",
    "snippet_highlighted_words": [
        "Basmati Rice",
        "1 kg",
        "1 kg",
        "1 kg"
    ],
    "rich_snippet": {
        "bottom": {
            "extensions": [
                "Free delivery"
            ]
        }
    },
    "source": "Flipkart"
}]

# loop through each product
for item in results:
    price = None

    # For BigBasket: check detected_extensions
    if (
        "rich_snippet" in item
        and "bottom" in item["rich_snippet"]
        and "detected_extensions" in item["rich_snippet"]["bottom"]
        and "price" in item["rich_snippet"]["bottom"]["detected_extensions"]
    ):
        price = item["rich_snippet"]["bottom"]["detected_extensions"]["price"]

    # For Flipkart: parse snippet text
    elif "snippet" in item and item["snippet"]:
        # Look for a ₹ sign followed by digits
        matches = re.findall(r"₹\s*([\d,\.]+)", item["snippet"])
        if matches:
            # take the last price mentioned (often the discounted price)
            price_str = matches[-1].replace(",", "")
            try:
                price = float(price_str)
            except:
                price = price_str

    print("Title:", item["title"])
    print("Image :", item["favicon"])
    print("Price:", price if price is not None else "N/A")
    print("---")
