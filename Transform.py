from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import os
# Setup chrome driver
driver = webdriver.Chrome()

def scroll_down():
    '''
    Using scroll access hidden element, navigator
    '''
    scroll_percentage = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_percentage)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Navigate to the url
driver.get('https://tiki.vn/do-choi-me-be/c2549')
# Add a delay to wait for the page to load
time.sleep(2)  # Adjust the delay as needed
# Find all div elements with specific class name
# Iterate over the divs
list_of_discounts = []
discount_elements = driver.find_elements(By.CSS_SELECTOR, ".price-discount")
current_time =  time.strftime("%Y%m%d_%H%M%S")
try:
    os.mkdir("export")
except:
    pass
os.mkdir(f"export/{current_time}")
for element in discount_elements:
    try:
        discount_element = element.find_element(By.CSS_SELECTOR, ".price-discount__discount")
        discount = discount_element.text
        list_of_discounts.append(discount)
    except NoSuchElementException:
        list_of_discounts.append("-0%")

print(len(list_of_discounts))
