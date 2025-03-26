from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Constants
LOGIN_URL = "https://qa.dashboard.everest.7span.in/#/login"
DASHBOARD_URL = "https://qa.dashboard.everest.7span.in/#/dashboard"
TIMESHEET_URL = "https://qa.dashboard.everest.7span.in/#/timesheet"
EMAIL = "kajal@7span.com"
PASSWORD = "1"
EMPLOYEE_NAME = "Krunal Baldha"

# XPath Selectors
EMAIL_INPUT = "//input[@id='email']"
PASSWORD_INPUT = "//input[@id='password']"
SIGNIN_BUTTON = "//button[@type='submit']"
PLAN_BUTTON = "//button[@id='radix-:rf:-trigger-plan']"
SEARCH_BAR = "//input[@id='search-Employee']"
SAVE_CHANGES_BUTTON = "//button[normalize-space()='Save Changes']"
CONFIRMATION_MESSAGE = "//p[normalize-space()='Changes saved successfully!']"
INPUT_BOXES_XPATH = "//input[contains(@id, 'headlessui-input')]"

# Initialize WebDriver
service = Service("chromedriver.exe")
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(LOGIN_URL)
wait = WebDriverWait(driver, 10)

# Login
print("🔐 Logging into Everest...")
wait.until(EC.element_to_be_clickable((By.XPATH, EMAIL_INPUT))).send_keys(EMAIL)
wait.until(EC.element_to_be_clickable((By.XPATH, PASSWORD_INPUT))).send_keys(PASSWORD)
driver.find_element(By.XPATH, SIGNIN_BUTTON).click()
print("✅ Login successful!")
wait.until(EC.url_contains(DASHBOARD_URL))
time.sleep(1)

# Navigate to Timesheet Module
print("📂 Navigating to Timesheet module...")
driver.get(TIMESHEET_URL)
wait.until(EC.element_to_be_clickable((By.XPATH, PLAN_BUTTON))).click()

# Search Employee
print(f"🔎 Searching for Employee - {EMPLOYEE_NAME}...")
search_box = wait.until(EC.element_to_be_clickable((By.XPATH, SEARCH_BAR)))
search_box.send_keys(EMPLOYEE_NAME)
time.sleep(2)
search_box.send_keys(Keys.ENTER)
print("✅ Employee found successfully!")
time.sleep(2)

# Scroll Down
actions = ActionChains(driver)
actions.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(2)

# Enter Planning Hours 
print("🔄 Moving All Planning Logs...")
input_boxes = driver.find_elements(By.XPATH, INPUT_BOXES_XPATH)

for i in range(1, 6):  # Monday to Friday
    if len(input_boxes) >= i:
        input_box = input_boxes[i - 1]  # List index starts from 0
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)  # Ensure visibility
        time.sleep(0.5)  # Small delay to allow UI to adjust
        input_box.clear()
        input_box.send_keys("4")
        time.sleep(1)  # Give time for input processing
    else:
        print(f"Skipping input {i}, not found!")

# Click Save and Verify
driver.find_element(By.XPATH, SAVE_CHANGES_BUTTON).click()
wait.until(EC.visibility_of_element_located((By.XPATH, CONFIRMATION_MESSAGE)))
print("✅ Changes saved successfully!")

# ================================
# **Remove Planning Hours - FIXED**
# ================================
print("Removing Planning Hours...")

input_boxes = driver.find_elements(By.XPATH, INPUT_BOXES_XPATH)

if not input_boxes:
    print("No input boxes found!")
else:
    for i in range(5):  # Only Monday to Friday (First 5 input fields)
        if i < len(input_boxes):  # Ensure index is within range
            input_box = input_boxes[i]

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)  # Scroll into view
            time.sleep(0.5)

            # **Fix 1: Ensure input box is clickable**
            try:
                wait.until(EC.element_to_be_clickable(input_box))
            except:
                print(f"⚠️ Input box {i + 1} not clickable. Skipping...")

            # **Fix 2: Use JavaScript click**
            driver.execute_script("arguments[0].click();", input_box)
            time.sleep(0.5)

            # **Fix 3: Clear using JavaScript**
            driver.execute_script("arguments[0].value = '';", input_box)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_box)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_box)
            time.sleep(0.5)

            # **Fix 4: Clear using Keyboard**
            input_box.send_keys(Keys.CONTROL + "a")  # Select all text
            input_box.send_keys(Keys.BACKSPACE)  # Delete selected text
            input_box.send_keys(Keys.ENTER)  # Confirm the change
            time.sleep(1)

            # Validate if the input box is empty
            current_value = input_box.get_attribute("value").strip()
            if current_value == "":
                print(f"✅ Planning hours cleared for input box {i + 1}.")
            else:
                print(f"⚠️ Warning: Input box {i + 1} still contains value '{current_value}'. Retrying...")

                # Try clearing again if needed
                input_box.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE, Keys.ENTER)
                time.sleep(1)

                # Re-check value after retry
                current_value = input_box.get_attribute("value").strip()
                if current_value == "":
                    print(f"✅ Input box {i + 1} cleared successfully after retry.")
                else:
                    print(f"❌ Error: Input box {i + 1} still contains '{current_value}'. Check React state.")

    print("✅ All planning hours removed successfully!")

# Click Save and Verify Again
save_button = driver.find_element(By.XPATH, SAVE_CHANGES_BUTTON)  
save_button.click()

# Wait for confirmation message
wait.until(EC.visibility_of_element_located((By.XPATH, CONFIRMATION_MESSAGE)))
print("✅ Changes saved successfully after removing hours!")

# Close WebDriver
time.sleep(3)
driver.quit()
