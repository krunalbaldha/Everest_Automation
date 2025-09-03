from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://qa.dashboard.everest.7span.in/#/login")
driver.maximize_window()

# Login Credentials
email = "kajal@7span.com"
password = "1"

# Login
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))).send_keys(email)
print("✅ Email entered")
driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
print("✅ Password entered")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
print("✅ Login Successful")
time.sleep(3)

# Navigate to Performance Module
print("🚀 Navigating to Performance Module...")
driver.get("https://qa.dashboard.everest.7span.in/#/performance")
print("✅ Performance Module Opened")
time.sleep(3)

# Navigate to Quadrimester 3
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(), 'FY 2024-25 - Quadrimester 3')]"))).click()
print("✅ Quadrimester 3 Opened")
time.sleep(2)

# Navigate to Kajal Pandya's Self Evaluation
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(), 'Kajal Pandya')]"))).click()
print("✅ Kajal Pandya's Self Evaluation Opened")
time.sleep(2)

# Ensure the "Self Evaluation" button is visible and clickable
try:
    self_evaluation_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Self Evaluation']"))
    )

    # Scroll into view (if needed)
    driver.execute_script("arguments[0].scrollIntoView(true);", self_evaluation_button)
    time.sleep(1)  # Allow some buffer time

    # Ensure it is clickable
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(self_evaluation_button)).click()
    print("✅ Self Evaluation Opened")
    time.sleep(3)

except Exception as e:
    print(f"❌ Error: {e}")
    driver.save_screenshot("error_screenshot.png")  # Capture screenshot for debugging

# Headings and their XPaths
headings = [
    "//p[normalize-space()='Teamwork']",
    "//p[normalize-space()='Communication']",
    "//p[normalize-space()='Giving and receiving feedback']",
    "//p[normalize-space()='Time management']",
    "//p[normalize-space()='Analytical Thinking']",
    "//p[normalize-space()='Building work relationships']",
    "//p[normalize-space()='Quality and technical Skills']",
    "//p[normalize-space()='Decision making']",
    "//p[normalize-space()='Process thinking']",
    "//p[normalize-space()='Mentoring']",
    "//p[normalize-space()='Business Acumen & Strategy']"
]

# Emoji selection XPaths
emojis = [
    "//span[contains(text(),'Never')]",
    "//span[contains(text(),'Rarely')]",
    "//span[contains(text(),'Sometimes')]",
    "//span[contains(text(),'Often')]",
    "//span[contains(text(),'Usually')]",
    "//span[contains(text(),'Almost Always')]",
    "//span[contains(text(),'Gold Standard')]"
]

# Iterate through each heading, verify it, and select a random emoji
for index, heading_xpath in enumerate(headings):
    try:
        # Wait until the heading is visible
        heading_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, heading_xpath))
        )
        print(f"✅ Navigated to Heading {index+1}: {heading_element.text}")

        # Select a random emoji from the list (Ensure emojis contain correct XPaths)
        random_emoji_xpath = random.choice(emojis)  # Select a random emoji from the list

        # Wait until the emoji is visible and clickable before interacting
        emoji_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, random_emoji_xpath))
        )
        
        # Scroll the emoji into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", emoji_element)
        time.sleep(1)  # Allow time for the element to be scrolled into view

        # Ensure it is clickable
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(emoji_element)).click()
        print(f"✅ Selected Emoji for Heading {index+1}")

        # Simulate user behavior
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error at Heading {index+1}: {e}")
        driver.save_screenshot(f"error_heading_{index+1}.png") 

# Close the browser after completion
time.sleep(3)
driver.quit()
