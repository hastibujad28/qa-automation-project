import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the directory for screenshots
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Log file path
log_file = "test_results.txt"

# Function to capture screenshots
def capture_screenshot(driver, test_name, status):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{status}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

# Function to log test results
def log_test_result(test_name, result):
    with open(log_file, "a") as file:
        file.write(f"{test_name}: {result}\n")
    print(f"Test result logged: {test_name} - {result}")

def test_flipkart_cart():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 30)
    test_name = "test_flipkart_cart"
    
    try:
        driver.get("https://www.flipkart.com")
        print("Opened Flipkart")
    
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("Samsung Galaxy")
        search_box.submit()
        print("Searched for Samsung Galaxy")
      
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            product = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/p/')]"))
            )
            product.click()
            print("Clicked on a product")
        except:
            print("Products did not load in time.")
            capture_screenshot(driver, test_name, "failed")
            log_test_result(test_name, "Failed: Products did not load in time.")
            return
    
        driver.switch_to.window(driver.window_handles[-1])

        try:
            add_to_cart = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add to cart')]"))
            )
            add_to_cart.click()
            print("Flipkart Cart Test Passed")
            capture_screenshot(driver, test_name, "passed")
            log_test_result(test_name, "Passed")
        except:
            print("Add to cart button not found.")
            capture_screenshot(driver, test_name, "failed")
            log_test_result(test_name, "Failed: Add to cart button not found.")
    except Exception as e:
        print(f"Test failed: {e}")
        capture_screenshot(driver, test_name, "failed")
        log_test_result(test_name, f"Failed: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_flipkart_cart()

