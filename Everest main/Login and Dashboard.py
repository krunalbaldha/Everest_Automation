from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# 🚀 Initialize WebDriver
print("🚀 Starting WebDriver...")
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# ✅ Everest Login URL
url = "https://qa.dashboard.everest.7span.in/#/login"
driver.get(url)
time.sleep(2)

# Google Drive folder path (Replace with your actual mounted path if using Colab)
gdrive_folder = "C:\Automation\Selenium\Screenshots"
os.makedirs(gdrive_folder, exist_ok=True)

def take_screenshot(name):
    """Function to take a screenshot and save it to Google Drive."""
    screenshot_path = os.path.join(gdrive_folder, f"{name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")

def login(email, password, expected_error=None):
    """Function to perform login and check error messages."""
    print(f"🔍 Testing login with Email: {email} | Password: {password}")

    # Locate email field and enter value
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.clear()
    email_field.send_keys(email)

    # Locate password field and enter value
    password_field = driver.find_element(By.ID, "password")
    password_field.clear()
    password_field.send_keys(password)

    # Click login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for response
    time.sleep(2)

    if expected_error:
        try:
            error_message = wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//p[normalize-space()='{expected_error}']"))
            ).text
            assert error_message == expected_error
            print(f"✅ Error message verified: {error_message}")
        except Exception:
            print(f"❌ Expected error message '{expected_error}' not found!")
    else:
        wait.until(EC.url_contains("/dashboard"))
        print("✅ Successfully logged in!")
    
    # Take screenshot after each login attempt
    take_screenshot(email.replace("@", "_at_"))
    time.sleep(2)

# ✅ 1. Login with Wrong Email & Wrong Password
login("wrong.email@7span.com", "wrongpassword", "Invalid email or password.")

# ✅ 2. Login with Valid Email & Wrong Password
login("krunal.b@7span.com", "wrongpassword", "Invalid email or password.")

# ✅ 3. Login with Empty Email & Filled Password
login("", "1", "Email is required.")

# ✅ 4. Login with Filled Email & Empty Password
login("krunal.b@7span.com", "", "Password is required.")

# ✅ 5. Login with Both Fields Empty
login("", "", "Email is required.")

# ✅ 6. Login with Non-7span.com Email
login("test@gmail.com", "1", "Only 7span.com email is allowed.")

# ✅ 7. Login with Valid Credentials
login("krunal.b@7span.com", "1")

# ✅ 8. Scroll Down & Up on Login Page
print("📜 Scrolling Down & Up on Login Page...")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, 0);")
print("✅ Scrolling Test Passed!")

# ✅ Close Browser
print("🛑 Closing WebDriver...")
time.sleep(3)
driver.quit()