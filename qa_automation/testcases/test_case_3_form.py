import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ensure the screenshot folder exists
screenshot_folder = "path_to_screenshot_folder"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Using WebDriver Manager to install ChromeDriver with chrome options
options = Options()
options.headless = False 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to take a screenshot
def take_screenshot(test_name):
    screenshot_path = os.path.join(screenshot_folder, f"{test_name}_screenshot.png")
    driver.get_screenshot_as_file(screenshot_path)

def test_apple_form():
    try:
        driver.get("https://account.apple.com/account")
        print("Waiting for page to load...")

        # Validate that the page loads and form fields are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "appleid"))
        )
        print("Form fields are visible.")

        # Submit a blank form and verify error messages
        submit_button = driver.find_element(By.ID, "submit_button")
        submit_button.click()
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "error_message"))
        )
        assert "This field is required" in error_message.text, "Error message not found for blank form"
        print("Error message displayed for blank form submission.")

        # Validate Email Format
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("invalid_email")
        submit_button.click()
        email_error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email_error_message"))
        )
        assert "Invalid email address" in email_error_message.text, "Email format error message not displayed"
        print("Error message displayed for invalid email format.")

        # Password Requirements
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("short")
        submit_button.click()
        password_error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password_error_message"))
        )
        assert "Password is too weak" in password_error_message.text, "Password strength error message not displayed"
        print("Error message displayed for weak password.")

        # Confirm Password Mismatch
        confirm_password_field = driver.find_element(By.ID, "confirm_password")
        confirm_password_field.send_keys("mismatch_password")
        submit_button.click()
        password_mismatch_error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password_mismatch_error_message"))
        )
        assert "Passwords do not match" in password_mismatch_error_message.text, "Password mismatch error message not displayed"
        print("Error message displayed for mismatched passwords.")

        # Submit valid data (if possible)
        email_field.clear()
        email_field.send_keys("valid_email@example.com")
        password_field.clear()
        password_field.send_keys("StrongPassword123")
        confirm_password_field.clear()
        confirm_password_field.send_keys("StrongPassword123")
        submit_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "success_message"))
        )
        print("Form submitted successfully with valid data.")

    except Exception as e:
        take_screenshot("apple_form_test_failed")
        print(f"Test failed: {e}")
        raise e  # Re-raise the exception after taking the screenshot
    finally:
        driver.quit()
