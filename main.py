from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    # update the path to the location of your Chrome binary
    CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    options = Options()
    # options.add_argument("--headless=new")
    options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(options=options)

    return driver


def get_all_pages_html(driver):

    #print(f"Getting data from {url}")

    #driver.get(url)
    # workaround to get the page source after initial 429 error
    #driver.get(url)
    #driver.maximize_window()

    # Wait for the page to load
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    # Inside get_raw_trends_data:
    """Clicks through all pagination and returns combined HTML from each page."""
    html_pages = []

    while True:
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "geo-widget-wrapper"))
        )
        time.sleep(1)

        html_pages.append(driver.page_source)

        try:
            # Try to find and click the next page arrow
            next_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
            if next_btn.is_enabled():
                next_btn.click()
            else:
                break
        except NoSuchElementException:
            break
        except TimeoutException:
            break

    return html_pages


# Add import
from bs4 import BeautifulSoup

def extract_interest_by_sub_region(content: str) -> dict:
    soup = BeautifulSoup(content, "html.parser")

    interest_by_subregion = soup.find("div", class_="geo-widget-wrapper geo-resolution-subregion")
    if interest_by_subregion is None:
        print("❌ Could not find interest_by_subregion container.")
        return {}

    related_queries = interest_by_subregion.find_all("div", class_="fe-atoms-generic-content-container")

    # Dictionary to store the extracted data
    interest_data = {}

    # Extract the region name and interest percentage
    for query in related_queries:
        items = query.find_all("div", class_="item")
        for item in items:
            region = item.find("div", class_="label-text")
            interest = item.find("div", class_="progress-value")
            if region and interest:
                interest_data[region.text.strip()] = interest.text.strip()

    return interest_data

# Parameters
date_range = "now 7-d"
geo = "US"
query = "zombies"

# Construct the URL
url = f"https://trends.google.com/trends/explore?date={date_range}&geo={geo}&q={query}"

driver = get_driver()

driver.get(url)
all_html = get_all_pages_html(driver)

interest_data = {}
for page_html in all_html:
    page_data = extract_interest_by_sub_region(page_html)
    interest_data.update(page_data)  # Merge dictionaries


# Print the extracted data
for region, interest in interest_data.items():
    print(f"{region}: {interest}")
