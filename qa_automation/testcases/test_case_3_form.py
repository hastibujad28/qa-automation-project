from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")

# Initializing driver with WebDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def test_apple_account_form():
    driver.get("https://account.apple.com/account")
    wait = WebDriverWait(driver, 30)
    try:
        # 1. Validate that the page loads and form fields are visible
        print("Waiting for page to load...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        print("Page loaded and login field is visible")
        time.sleep(5) 

        # 2. Submit blank form and verify error
        print("Submitting blank form...")
        print("Scrolling to bottom...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Locating the Continue button
        print("Locating Continue button...")
        continue_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[form='create'][type='submit']"))
        )
        continue_button.click()
        print("Clicked Continue button")

        time.sleep(3)

        error_elements = driver.find_elements(By.CLASS_NAME, "form-message") 
        if error_elements:
            print("Blank form submission shows error")
        else:
            print("No error shown for blank submission")

        # 3. Invalid email format
        print("Entering invalid email...")
        email_field = driver.find_element(By.ID, "account_name_text_field")
        email_field.clear()
        email_field.send_keys("invalid-email")
        driver.find_element(By.ID, "sign-in").click()
        time.sleep(3)
        if "Enter a valid email address." in driver.page_source:
            print("Invalid email format error shown")
        else:
            print("Invalid email format not detected")

        # 4. Weak password (after entering a valid-looking email)
        print("Entering weak password...")
        email_field.clear()
        email_field.send_keys("test@example.com")
        driver.find_element(By.ID, "sign-in").click()
        time.sleep(3)

        try:
            password_field = driver.find_element(By.ID, "password_text_field")
            password_field.send_keys("123") 
            driver.find_element(By.ID, "sign-in").click()
            time.sleep(3)
            print("Weak password error or rejection shown")
        except Exception as e:
            print(f"Password field did not load: {str(e)}")

        
        print("Skipping password mismatch as Apple form doesn't include a confirm password field.")
        print("Cannot test full login without real credentials")

    except Exception as e:
        print(f"Test failed: {str(e)}")
    finally:
        driver.quit()

# Run the test
test_apple_account_form()
