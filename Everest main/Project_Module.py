from concurrent.futures import thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Constants
LOGIN_URL = "https://qa.dashboard.everest.7span.in/#/login"
DASHBOARD_URL = "https://qa.dashboard.everest.7span.in/#/dashboard"
PROJECT_MODULE_URL = "https://qa.dashboard.everest.7span.in/#/projects"

EMAIL = "kajal@7span.com"
PASSWORD = "1"
PROJECT_NAME = "NeuraBot X"
MILESTONE_NAME = "NB-X-Prototyping"
COORDINATOR_NAME = "Kajal Pandya"
SALES_PERSON_NAME = "Krunal Baldha"

# -------------------------------
# Login Process  
# -------------------------------
driver.get(LOGIN_URL)

wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))).send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
print("✅ Login: Success")

# Wait for Dashboard to Load
wait.until(EC.url_to_be(DASHBOARD_URL))

# -------------------------------
# Navigate to Project Module
# -------------------------------
driver.get(PROJECT_MODULE_URL)
print("✅ Project Module Navigate Successfully")

# Click "In Progress"
wait.until(EC.element_to_be_clickable((By.XPATH, "//body//div//dl//a[2]"))).click()
print("✅ Click In Progress Button")

# -------------------------------
# Open and Reset Filter
# -------------------------------
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'inline-flex')]//*[name()='svg']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Clear All']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='absolute -inset-2.5']"))).click()
print("✅ Filter Closed Successfully")

# -------------------------------
# Search for Project
# -------------------------------
# Ensure the search bar is visible and interactable
search_bar = wait.until(EC.visibility_of_element_located((By.ID, "search-input")))

# Scroll into view to make sure it is visible
driver.execute_script("arguments[0].scrollIntoView(true);", search_bar)

# Click on the search bar to activate it (if needed)
search_bar.click()

# Send keys to search
search_bar.send_keys("Vepaar", Keys.ENTER)
time.sleep(2)

# Wait for "Data not found" message
wait.until(EC.text_to_be_present_in_element(
    (By.XPATH, "//div[contains(@class,'text-center flex justify-center items-center min-h-60')]"),
    "Data not found"
))
print("✅ Search result for 'Vepaar': Data not found")
time.sleep(3)

# -------------------------------
# Search for the Correct Project
# -------------------------------
search_bar = wait.until(EC.element_to_be_clickable((By.ID, "search-input")))
driver.execute_script("arguments[0].value = '';", search_bar)
search_bar.send_keys(PROJECT_NAME, Keys.ENTER)
time.sleep(3)

# Wait for results
results = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody//tr")))

if not results:
    print(f"❌ No results found for {PROJECT_NAME}")
    driver.quit()
    exit(1)

assert PROJECT_NAME in results[0].text, f"❌ Search did not return the correct project for '{PROJECT_NAME}'"
print(f"✅ Search Result for '{PROJECT_NAME}':", results[0].text)
time.sleep(1)

#Search bar Clear functions

# Ensure the search bar is cleared properly
search_bar.send_keys(Keys.CONTROL + "a")  # Select all text
search_bar.send_keys(Keys.DELETE)  # Delete the text
time.sleep(2)

### Add Sub Comment for the below code


# Verify the search bar is empty
assert search_bar.get_attribute("value") == "", "Search bar is not cleared properly"
print("✅ Search bar cleared successfully")

# -------------------------------
# Apply Filters: Coordinator, Sales Person, Status
# -------------------------------
print("📍 Applying Filters...")
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'inline-flex')]//*[name()='svg']"))).click()

coordinator_input = wait.until(EC.element_to_be_clickable((By.ID, "search-Co-ordinator")))
coordinator_input.send_keys(COORDINATOR_NAME)
wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{COORDINATOR_NAME}')]"))).click()
time.sleep(1)
print("✅ Coordinator Filter Applied")

sales_person_input = wait.until(EC.element_to_be_clickable((By.ID, "search-Sales Person")))
sales_person_input.send_keys(SALES_PERSON_NAME)
wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{SALES_PERSON_NAME}')]"))).click()
time.sleep(1)
print("✅ Sales Person Filter Applied")

status_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "search-Status")))
status_dropdown.click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'In Progress')]"))).click()
time.sleep(1)
print("✅ Status Filter Applied")

# Apply Filters
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Apply']"))).click()
time.sleep(1)
print("✅ Filters Applied Successfully")

# -------------------------------
# Select the Project & Open Dashboard
# -------------------------------
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div/main/div/div/div/main/div/div[3]/div/div/table/tbody/tr/td[1]/a"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Dashboard']"))).click()
time.sleep(2)
print("✅ Project Selected & Dashboard Opened")

# -------------------------------
# Navigate to Milestone
# -------------------------------
print("📍 Navigating to Milestones...")
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Milestones')]"))).click()
time.sleep(2)
print("✅ Milestones Opened")

# Search Milestone
print("📍 Searching for Milestone...")
milestone_search = wait.until(EC.presence_of_element_located((By.ID, "search-input")))
milestone_search.send_keys(MILESTONE_NAME)
wait.until(EC.text_to_be_present_in_element((By.XPATH, "//tbody"), MILESTONE_NAME))
time.sleep(2)
print("✅ Milestone Found")

# Clear search field
milestone_search.send_keys(Keys.CONTROL + "a", Keys.DELETE)
time.sleep(2)
print("✅ Search Field Cleared")

# -------------------------------
# Filter Milestone Type & Status
# -------------------------------

# Milestone Type Dropdown

try:
    # ✅ Ensure the dropdown is interactable before clicking
    milestone_type_dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='All Types'])[1]"))
    )
    time.sleep(2)
    # Use JavaScript if normal click doesn't work
    driver.execute_script("arguments[0].click();", milestone_type_dropdown)
    print("✅ Milestone Type Dropdown Opened")

    free_option = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@id, 'headlessui-menu-item')]"))
)
    # ✅ Iterate over options to find the one containing "Free"
    for option in free_option:
        if "Free" in option.text:
            driver.execute_script("arguments[0].click();", option)
            print("✅ Clicked on 'Free' option successfully!")
            break
    else:
        print("❌ 'Free' option not found!")

except Exception as e:
    print(f"❌ Error: {e}")
time.sleep(2)

# Milestone Status Dropdown

try:
    # ✅ Ensure the dropdown is interactable before clicking
    milestone_status_dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='All Status'])[1]"))       
    )  
    # Use JavaScript if normal click doesn't work
    driver.execute_script("arguments[0].click();", milestone_status_dropdown)
    print("✅ Milestone Type Dropdown Opened")

    in_progress_option = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@id, 'headlessui-menu-item')]"))
)
    # ✅ Iterate over options to find the one containing "Free"
    for option in in_progress_option:
        if "In Progress" in option.text:
            driver.execute_script("arguments[0].click();", option)
            print("✅ Clicked on 'In Progrees' option successfully!")
            break
    else:
        print("❌ 'In Progress' option not found!")

except Exception as e:
    print(f"❌ Error: {e}")

time.sleep(2)

# ✅ Wait for the element to be clickable
first_milestone = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]//td[1]"))
)
time.sleep(5)

try:
    # ✅ Wait until the element is clickable
    first_milestone = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'absolute inset-0 focus:outline-none')]"))
    )

    # ✅ Scroll into view
    driver.execute_script("arguments[0].scrollIntoView(true);", first_milestone)
    time.sleep(1)  # Allow UI to adjust

    # ✅ Click using JavaScript to avoid interception
    driver.execute_script("arguments[0].click();", first_milestone)
    print("✅ Milestone details opened successfully!")

    time.sleep(2)

    # ✅ Scroll Down to the Bottom
    driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
    time.sleep(2)  # Allow time for scrolling to complete

    # ✅ Scroll Up to the Top
    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    time.sleep(2)
    
    # ✅ Close Browser
    driver.quit()
    print("✅ Test Case Passed Successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

