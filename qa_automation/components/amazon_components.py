from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonComponents:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search_item(self, term):
        search_box = self.wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.clear()
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)

    def get_search_results(self):
        return self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")))

    def open_product(self, index):
        results = self.get_search_results()
        if index < len(results):
            results[index].find_element(By.TAG_NAME, "a").click()

    def validate_product_details(self):
        title = self.wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text
        price = self.driver.find_element(By.CSS_SELECTOR, "span.a-price > span.a-offscreen").text
        availability = self.driver.find_element(By.ID, "availability").text
        return title, price, availability

    def add_to_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button"))).click()

    def go_to_cart(self):
        self.driver.get("https://www.amazon.in/gp/cart/view.html")

    def get_cart_item_details(self):
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-truncate-cut"))).text
        price = self.driver.find_element(By.CSS_SELECTOR, "span.sc-product-price").text
        return title, price

    def remove_from_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Delete']"))).click()
