import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_amazon_product_url(query):
    search_url = f"https://www.amazon.in/s?k={quote_plus(query)}"
    response = requests.get(search_url, headers=HEADERS)
    
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.select_one("div.s-main-slot a.a-link-normal.s-no-outline")
    if link:
        return "https://www.amazon.in" + link["href"]
    return None


def get_bigbasket_products(query):
    search_url = f"https://www.bigbasket.com/ps/?q={quote_plus(query)}"
    
    response = requests.get(search_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # Find product cards
    product_cards = soup.select("a.ProductCard__StyledProductLink-sc-d3svbp-7")
    
    print(product_cards)
    
    results = []

    for card in product_cards:
        # Product name
        name_elem = card.select_one("div.ProductCard__ProductName-sc-d3svbp-10")
        title = name_elem.text.strip() if name_elem else "N/A"

        # Price
        price_elem = card.select_one("span.DiscountedPrice__StyledPrice-sc-d0s3ms-1")
        price = price_elem.text.strip() if price_elem else "N/A"

        # Image
        image_elem = card.find("img")
        image = image_elem["src"] if image_elem else "N/A"

        # Product link
        # link = "https://www.bigbasket.com" + card["href"]

        results.append({
            "title": title,
            "price": price,
            "image": image
            # ,
            # "link": link
        })

    return results


def get_amazon_details(product_url):
    response = requests.get(product_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find(id="productTitle")
    price = soup.find("span", class_="a-price-whole")
    image_tag = soup.find("img", id="landingImage")

    return {
        "title": title.text.strip() if title else "N/A",
        "price": price.text.strip() if price else "N/A",
        "image": image_tag["src"] if image_tag else "N/A"
        # ,"link": product_url
    }


# def get_flipkart_details(product_url):
#     response = requests.get(product_url, headers=HEADERS)
#     soup = BeautifulSoup(response.text, "html.parser")
#     print(soup)
#     title = soup.find("span", class_="B_NuCI")
#     price = soup.find("div", class_="_30jeq3 _16Jk6d")
#     image_tag = soup.select_one("img._396cs4._2amPTt._3qGmMb") or soup.select_one("img._2r_T1I")  # support different layouts

#     return {
#         "title": title.text.strip() if title else "N/A",
#         "price": price.text.strip() if price else "N/A",
#         "image": image_tag["src"] if image_tag else "N/A"
#         # ,"link": product_url
#     }


def compare_prices_with_images(query):
    print(f"🔍 Searching for: {query}\n")

    # Amazon
    # amazon_url = get_amazon_product_url(query)
    # if amazon_url:
    #     details = get_amazon_details(amazon_url)
    #     print("🛒 Amazon:")
    #     print(f"  Title : {details['title']}")
    #     print(f"  Price : ₹{details['price']}")
    #     print(f"  Image : {details['image']}")
    #     # print(f"  Link  : {details['link']}\n")
    # else:
    #     print("Amazon product not found.\n")

    details = get_bigbasket_products(query)
    if details:
        print("🛒 bigbasket:")
        print(f"  Title : {details['title']}")
        print(f"  Price : ₹{details['price']}")
        print(f"  Image : {details['image']}")
        # print(f"  Link  : {details['link']}\n")
    else:
        print("bigbasket product not found.\n")
    # Flipkart
    # flipkart_url = get_flipkart_product_url(query)
    # if flipkart_url:
    #     details = get_flipkart_details(flipkart_url)
    #     print("🛍️ Flipkart:")
    #     print(f"  Title : {details['title']}")
    #     print(f"  Price : {details['price']}")
    #     print(f"  Image : {details['image']}")
    #     # print(f"  Link  : {details['link']}\n")
    # else:
    #     print("Flipkart product not found.\n")

query = "basmati rice 1kg"
compare_prices_with_images(query)
# 🔧 Example usage
# if __name__ == "_main_":
#     query = "1 kg Basmati Rice"
#     compare_prices_with_images(query)