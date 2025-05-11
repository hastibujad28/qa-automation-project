from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AppleComponents:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_account_page(self):
        self.driver.get("https://account.apple.com/account")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

    def submit_blank_form(self):
        self.driver.find_element(By.TAG_NAME, "form").submit()

    def input_email(self, email):
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "account_name_text_field")))
        email_field.clear()
        email_field.send_keys(email)

    def input_password(self, password):
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password_text_field")))
        password_field.clear()
        password_field.send_keys(password)

    def get_errors(self):
        errors = self.driver.find_elements(By.CSS_SELECTOR, ".error")
        return [e.text for e in errors if e.text.strip() != ""]
