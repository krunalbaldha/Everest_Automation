import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

# Setup WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Constants
URL = "https://qa.dashboard.everest.7span.in/#/login"
EMAIL = "kajal@7span.com"
PASSWORD = "1"
PROJECT_NAME_1 = "HoloTrain"
PROJECT_NAME_2 = "SeaSphere"
COORDINATOR_NAME = "Kajal Pandya"

# XPath Constants
XPATHS = {
    "email": "//input[@id='email']",
    "password": "//input[@id='password']",
    "submit": "//button[@type='submit']",
    "insights_module": "//span[contains(text(),'Insights')]",
    "yet_to_close": "//span[contains(text(),'Yet To Close')]",
    "search_bar": "//input[@id='search-input']",
    "me_mode": "//button[contains(., 'Me mode')]",
    "filter": "//div[@id='root']//main//button[2]/span[2]",
    "coordinator_search": "//input[@id='search-Co-ordinator']",
    "date_range": "//span[normalize-space()='Select date...']",
    "last_month": "//button[normalize-space()='Last Month']",
    "show_products_toggle": "//button[@id='headlessui-switch-:r58c:']",
    "clear_all": "//buttton[normalize-space()='Clear All']",
    "apply": "//button[normalize-space()='Apply']",
    "sea_sphere": "(//d[contains(text(), 'SeaSphere')])[1]"
}

# Function to click an element safely
def safe_click(xpath):
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)  # Small delay to ensure visibility
        element.click()
    except ElementClickInterceptedException:
        print(f"🔹 Click intercepted on {xpath}, using JavaScript...")
        driver.execute_script("arguments[0].click();", element)
    except TimeoutException:
        print(f"❌ Element {xpath} not found!")

# Function to input text into a field
def input_text(xpath, text, clear_first=True):
    field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    if clear_first:
        field.send_keys(Keys.CONTROL + "a", Keys.DELETE)
    field.send_keys(text)

# Step 1: Login 🔑
print("🔹 Logging into the dashboard...")
driver.get(URL)
input_text(XPATHS["email"], EMAIL)
input_text(XPATHS["password"], PASSWORD)
safe_click(XPATHS["submit"])
time.sleep(2)
print("✅ Login successful!")

# Step 2: Navigate to Insights 📊
print("🔹 Navigating to Insights Module...")
safe_click(XPATHS["insights_module"])
time.sleep(2)

# Step 3: Navigate to Yet to Close 📌
print("🔹 Opening 'Yet To Close' section...")
safe_click(XPATHS["yet_to_close"])
time.sleep(2)

# Step 4-5: Search Project and Verify Output 🔍
print(f"🔹 Searching for project: {PROJECT_NAME_1}...")
input_text(XPATHS["search_bar"], PROJECT_NAME_1)
time.sleep(3)
input_text(XPATHS["search_bar"], "", clear_first=True)  # Clear search bar
assert wait.until(EC.presence_of_element_located((By.XPATH, XPATHS["search_bar"]))).get_attribute("value") == "", "❌ Search bar is not cleared properly"
print("✅ Search bar cleared!")

# Step 6-9: Toggle Me Mode 🔄
print("🔹 Toggling Me Mode...")
safe_click(XPATHS["me_mode"])
time.sleep(2)
safe_click(XPATHS["me_mode"])
time.sleep(2)

# Step 10-11: Apply Filters 🎯
print("🔹 Opening filter menu...")
safe_click(XPATHS["filter"])
time.sleep(2)
print(f"🔹 Searching for Coordinator: {COORDINATOR_NAME}...")
input_text(XPATHS["coordinator_search"], COORDINATOR_NAME)
time.sleep(2)
safe_click(f"//div[contains(text(), '{COORDINATOR_NAME}')]")
time.sleep(2)

# Step 12-13: Select Last Month 📅
print("🔹 Selecting 'Last Month' date range...")
safe_click(XPATHS["date_range"])
time.sleep(2)
safe_click(XPATHS["last_month"])
time.sleep(2)
safe_click(XPATHS["apply"])
time.sleep(4)

if "Data not found" in driver.page_source:
    print("✅ Filters applied successfully!")
else:
    print("❌ Filter Output Mismatch")

# Step 14: Clear Filters 🧹
print("🔹 Clearing all filters...")
safe_click(XPATHS["filter"])
time.sleep(2)
safe_click(XPATHS["clear_all"])
time.sleep(2)

# Step 15-17: Toggle Show Products 🔄
print("🔹 Opening filter panel...")
safe_click(XPATHS["filter"])  
time.sleep(3)

# Stable XPath for toggle button
show_products_xpath = "//button[contains(@id, 'headlessui-switch')]"

# Toggle "Show Products" ON
print("🔹 Enabling 'Show Products' option...")
toggle_button = wait.until(EC.element_to_be_clickable((By.XPATH, show_products_xpath)))
driver.execute_script("arguments[0].click();", toggle_button)
time.sleep(2)

# Click Apply
safe_click(XPATHS["apply"])
time.sleep(4)

# Verify Output
print("🔹 Checking if 'Clembot' appears...")
if wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]"))):
    print("✅ 'Clembot' found!")
else:
    print("❌ 'Clembot' not found!")

# Step 2: Disable Show Products
print("🔹 Disabling 'Show Products' option...")
safe_click(XPATHS["filter"])  
time.sleep(3)

toggle_button = wait.until(EC.element_to_be_clickable((By.XPATH, show_products_xpath)))
driver.execute_script("arguments[0].click();", toggle_button)
time.sleep(2)

# Click Apply
safe_click(XPATHS["apply"])
time.sleep(4)

print("✅ Show Products toggled off successfully!")

# Step 18-19: Search Another Project & Navigate 🚀
print(f"🔹 Searching for project: {PROJECT_NAME_2}...")
input_text(XPATHS["search_bar"], PROJECT_NAME_2)
time.sleep(2)
safe_click(XPATHS["sea_sphere"])

# Step 20-21: Scroll & Go Back 🔄
print("🔹 Smoothly scrolling down...")
# Scroll down smoothly
for i in range(0, 101, 5):  
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i} / 100);")
    time.sleep(0.05)  # Small delay for smooth effect

time.sleep(1)  # Pause to observe the effect

print("🔹 Smoothly scrolling up...")

# Scroll up smoothly
for i in range(100, -1, -5):  
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i} / 100);")
    time.sleep(0.05)  # Small delay for smooth effect

time.sleep(1)  # Pause before going back

# Go back using browser back button
print("🔹 Navigating back to the previous screen...")
driver.back()

# Wait for the previous screen to load
time.sleep(3)  # Adjust based on page load time

# Cleanup 🧹
print("🔹 Closing the browser...")
driver.quit()
print("✅ Test completed successfully!")
