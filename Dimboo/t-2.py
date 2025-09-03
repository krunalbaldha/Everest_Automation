from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# --- Configuration ---
URL = "https://zurolife.dev.dimboo.io/login/"
LOGIN_ID = "zuro.brand@dimboo.io"
PASSWORD = "7890"

# --- XPaths ---
login_field = "//input[@name='email']"
password_field = "//input[@placeholder='******']"
company_dropdown_icon = "//div[@id='downshift-:r1:-toggle-button']"  # FIXED
zuro_studio_option = "//span[normalize-space()='ZURO STUDIO - Belgium']"
influencers_module = "//p[contains(text(),'Influencers')]"
campaign_management_xpath = "//p[contains(text(),'Campaign Management')]"
logout_btn = "//span[normalize-space()='Logout']"

# --- Selenium Setup ---
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Open login page
    print("Opening login page... ")
    driver.get(URL)

    # Step 2: Login
    print("Entering login credentials...")
    wait.until(EC.presence_of_element_located((By.XPATH, login_field))).send_keys(LOGIN_ID)
    wait.until(EC.presence_of_element_located((By.XPATH, password_field))).send_keys(PASSWORD + Keys.RETURN)
    print("✅ Login submitted successfully.")

    # Step 3: Select Company from dropdown
    print("✅ Waiting for overlay to disappear...")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.backdrop-blur-sm")))
    except:
        print("⚠️ No overlay detected, continuing...")

    print("✅ Selecting company: Zuro Studio...")
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, company_dropdown_icon)))
    
    try:
        dropdown.click()
    except:
        driver.execute_script("arguments[0].click();", dropdown)
    
    wait.until(EC.element_to_be_clickable((By.XPATH, zuro_studio_option))).click()
    print("✅ Company selected successfully: Zuro Studio.")
    time.sleep(2)

    # Step 4: Navigate to Influencers → Campaign Management
    print("🧭 Navigating to Influencers Module...")
    wait.until(EC.element_to_be_clickable((By.XPATH, influencers_module))).click()
    print("✅ Influencers Module opened successfully.")

    print("✅ Opening Campaign Management...")
    wait.until(EC.element_to_be_clickable((By.XPATH, campaign_management_xpath))).click()
    print("✅ Campaign Management opened successfully.")

    time.sleep(2)

    # Step 5: Logout
    print("Logging out...")
    wait.until(EC.element_to_be_clickable((By.XPATH, logout_btn))).click()
    print("Logout successful.")

finally:
    print("Closing browser...")
    # time.sleep()
    driver.quit()
    print("Test completed ✅")
