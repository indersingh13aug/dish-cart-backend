from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus
import time

def get_flipkart_product_url_selenium(query):
    search_url = f"https://www.flipkart.com/search?q={quote_plus(query)}"

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")         # run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(search_url)

    # wait for results to load
    try:
        # This selector matches tiles in Flipkart search results
        product_link_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "a._1fQZEK, a.IRpwTa"
            ))
        )
    except Exception as e:
        print("No product links found.")
        driver.quit()
        return None

    product_url = product_link_elem.get_attribute("href")

    driver.quit()

    return product_url


def get_flipkart_details_selenium(product_url):
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(product_url)

    # Wait for title
    try:
        title_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "span.B_NuCI"
            ))
        )
        title = title_elem.text.strip()
    except:
        title = "N/A"

    # Wait for price
    try:
        price_elem = driver.find_element(By.CSS_SELECTOR, "div._30jeq3._16Jk6d")
        price = price_elem.text.strip()
    except:
        price = "N/A"

    # Wait for image
    try:
        image_elem = driver.find_element(By.CSS_SELECTOR, "img._396cs4._2amPTt._3qGmMb, img._2r_T1I")
        image_url = image_elem.get_attribute("src")
    except:
        image_url = "N/A"

    driver.quit()

    return {
        "title": title,
        "price": price,
        "image": image_url,
        "link": product_url
    }


def compare_prices_with_images(query):
    print(f"🔍 Searching for: {query}\n")

    flipkart_url = get_flipkart_product_url_selenium(query)
    if flipkart_url:
        details = get_flipkart_details_selenium(flipkart_url)
        print("🛍️ Flipkart:")
        print(f"  Title : {details['title']}")
        print(f"  Price : {details['price']}")
        print(f"  Image : {details['image']}")
        print(f"  Link  : {details['link']}\n")
    else:
        print("Flipkart product not found.\n")


query = "basmati rice 1kg"
compare_prices_with_images(query)

# if __name__ == "__main__":
#     query = "basmati rice 1kg"
#     compare_prices_with_images(query)
