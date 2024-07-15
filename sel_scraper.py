import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
webdriver_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

driver.get("https://t.me/the_h_club/37")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
iframe = soup.find("iframe")

if iframe:
    iframe_element = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe_element)

    iframe_content = driver.page_source
    iframe_soup = BeautifulSoup(iframe_content, "html.parser")
    image_wrap = iframe_soup.find("a", class_="tgme_widget_message_photo_wrap")

    if image_wrap and "style" in image_wrap.attrs:
        style_attr = image_wrap["style"]
        # Use regex to find the URL
        match = re.search(r'url\("(.+?)"\)', style_attr)
        if match:
            image_url = match.group(1)
            print("Background Image URL:", image_url)
        else:
            print("Background Image URL not found in style attribute")
    else:
        print("Image wrap not found or doesn't have style attribute")
#     anchor_tags = iframe_soup.find_all("a")
#
#     print("Anchor tags in the iframe:", anchor_tags)
#
#     # Switch back to the main content
#     driver.switch_to.default_content()
#
#     image_wrap = soup.find("a", class_="tgme_widget_message_photo_wrap")
#     if image_wrap and "style" in image_wrap.attrs:
#         style_attr = image_wrap["style"]
#         url_start = style_attr.find("url(&quot;") + len("url(&quot;")
#         url_end = style_attr.find("&quot;)", url_start)
#         image_url = style_attr[url_start:url_end]
#         print("Image URL:", image_url)
#     else:
#         print("Image URL not found")
# else:
#     print("No iframe found")

driver.quit()
