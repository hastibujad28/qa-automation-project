import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the directory for screenshots
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

# Log file path
log_file = "test_results.txt"

# Using WebDriver Manager to install ChromeDriver
service = Service(ChromeDriverManager().install())

# Initializing the Chrome driver with the Service object
driver = webdriver.Chrome(service=service)

# Function to capture screenshots on failure
def capture_screenshot(driver, test_name):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

# Function to log test results
def log_test_result(test_name, result):
    with open(log_file, "a") as file:
        file.write(f"{test_name}: {result}\n")
    print(f"Test result logged: {test_name} - {result}")

# Test case for Amazon search
def test_amazon_search():
    try:
        driver.get("https://www.amazon.com")

        # Wait for the search box to be present and visible
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        
        # Search for a product
        search_box.send_keys("laptop")
        search_box.submit()

        # Validate results
        assert "laptop" in driver.title
        print("Amazon Search Test Passed")
        log_test_result("test_amazon_search", "Passed")
    except Exception as e:
        capture_screenshot(driver, "test_amazon_search")
        log_test_result("test_amazon_search", f"Failed: {str(e)}")
        print(f"Test failed: {str(e)}")

# Run the test
test_amazon_search()

# Quit the driver
driver.quit()
