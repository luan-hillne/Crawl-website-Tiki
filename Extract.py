from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pandas as pd
import time
import os
driver = webdriver.Chrome()
def scroll_down():
    #Using scroll access hidden element, navigator
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

def rating_product(product_link):
    driver.get(product_link)
    rating_elements = driver.find_elements(By.CLASS_NAME,"review-rating__point")
    return [rating.text for rating in rating_elements]
def scraping_data_product(link,count,current_time,index):
    #driver.get(f'{link}?page={count}')
    driver.get(link)
    sleep(2)
    scroll_down()
    search_items_elements = driver.find_elements(By.CLASS_NAME,"style__ProductLink-sc-7xd6qw-2.fHwskZ.product-item")

    if search_items_elements == []:
        print("No find link product")
        return 0
    # Extract product details
    name_element = driver.find_elements(By.CSS_SELECTOR,".style__StyledNameProduction-sc-7xd6qw-4.dDfbLj")
    sold_element = driver.find_elements(By.CSS_SELECTOR,".style__StyledRatingList-sc-7xd6qw-6.eMNcac")
    price_element = driver.find_elements(By.CSS_SELECTOR, ".price-discount__price")
    discount_elements = driver.find_elements(By.CSS_SELECTOR,".price-discount")
    rating_ls_element = driver.find_elements(By.CLASS_NAME, "style__ProductLink-sc-7xd6qw-2.fHwskZ.product-item")

    def get_name():
        # Extract name
        return [name.text for name in name_element]

    def get_sold():
        # Extract sold product
        return [sold.text for sold in sold_element]

    def get_price():
        # Extract price
        return [price.text for price in price_element]

    list_of_discounts = []
    def get_discount():
        for element in discount_elements:
            try:
                discount_element = element.find_element(By.CSS_SELECTOR, ".price-discount__discount")
                discount = discount_element.text
                list_of_discounts.append(discount)
            except NoSuchElementException:
                list_of_discounts.append("-0%")
        return list_of_discounts

    def get_rating():
        return [category.get_attribute("href") for category in rating_ls_element]

    def save_dataframe():
        df_dict ={
            "name_product":get_name(),
            "sold_product":get_sold(),
            "price_product":get_price(),
            "discount_product":get_discount(),
            "link_product":get_rating()
        }
        df = pd.DataFrame(df_dict, columns=["name_product", "price_product", "sold_product", "discount_product","link_product"])
        df.to_csv(f'export/{current_time}/0{index}/data_{count}.csv', index=False)
        #print(df)
        return df
    save_dataframe()

    # len_page = len(get_sold())
    # return len_page
def scraping_link(ls_link):
    driver.get(ls_link)
    sleep(2)
    scroll_down()
    # Extract the links of sub-categories
    item_link_elements = driver.find_elements(By.CLASS_NAME, "item.item--category")
    return [item_link.get_attribute('href') for item_link in item_link_elements]
def scarp_data():
    current_time = time.strftime("%Y%m%d_%H%M%S")
    try:
        os.mkdir("export")
    except:
        pass
    os.mkdir(f"export/{current_time}")

    url = "https://tiki.vn/"
    driver.get(url)
    #Wait for some time to let the content load
    sleep(1)
    scroll_down()
    #Get attribute href of anchor tag and remove link advertise
    category_elements = driver.find_elements(By.CLASS_NAME, "styles__StyledItem-sc-oho8ay-0.bzmzGe")
    category_url_ls = [category.get_attribute('href') for category in category_elements if "/c" in category.get_attribute('href')]
    #print(category_url_ls)
    len_item = 0

    for index, ls_link in enumerate(category_url_ls):
        os.mkdir(f"export/{current_time}/0{index}")
        category_link = scraping_link(ls_link)
        #print(category_link)
        for count, link in enumerate(category_link):
            #print(link)
            item = scraping_data_product(link,count,current_time,index)
            if item == 0:
                break

if __name__ == "__main__":
    scarp_data()