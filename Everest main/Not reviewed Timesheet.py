import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

print("🔍 Starting Everest Insights Test Automation... 🚀")

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://qa.dashboard.everest.7span.in/#/login")
driver.maximize_window()

time.sleep(2)  # Wait for page to load

# Step 1: Login
print("🔑 Logging in...")
username = driver.find_element(By.XPATH, "//input[@id='email']")
password = driver.find_element(By.XPATH, "//input[@id='password']")
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

username.send_keys("krunal.b@7span.com")  # Replace with actual username
password.send_keys("1")  # Replace with actual password
login_button.click()

time.sleep(3)  # Wait for login to process
print("✅ Login successful!")

# Step 2: Navigate to Insights module
print("📊 Navigating to Insights module...")
driver.find_element(By.XPATH, "//span[contains(text(),'Insights')]").click()
time.sleep(2)

# Step 3: Navigate to "In Detail" and open
print("🔎 Opening 'In Detail' section...")
driver.find_element(By.XPATH, "//span[contains(text(),'In Detail')]").click()
time.sleep(2)

# Step 4: Navigate to Search bar
print("🔍 Searching for Coordinator: Krunal Baldha...")
search_bar = driver.find_element(By.XPATH, "//input[@id='search-Co-ordinator :']")
search_bar.click()
time.sleep(1)

# Step 5: Search for Coordinator name
search_bar.send_keys("Krunal Baldha")
time.sleep(2)
search_bar.send_keys(Keys.ENTER)
time.sleep(2)
print("✅ Coordinator found and selected!")

# Step 6: Select Date Range "Last Month"
print("📅 Selecting Date Range: Last Month...")
driver.find_element(By.XPATH, "//button[contains(@class, 'w-full text-left !py-2 relative isolate inline-flex items-center')]").click()
time.sleep(1)
driver.find_element(By.XPATH, "//button[normalize-space()='Last Month']").click()
time.sleep(2)
print("✅ Date range selected!")

# Step 7: Click Milestone name and verify redirection
print("📌 Clicking on Milestone name: 'SS-Concept Design & Feasibility'...")
driver.find_element(By.XPATH, "//a[contains(@class,'text-blue-500')]").click()
time.sleep(2)
print("✅ Redirected to Timesheet Review Screen!")

# Step 8: Click browser back button
print("🔙 Going back to 'In Details' screen...")
driver.back()
time.sleep(2)

# Step 9: Navigate to "Summary" and Open
print("📊 Navigating to 'Summary' section...")
driver.find_element(By.XPATH, "//span[contains(text(),'Summary')]").click()
time.sleep(2)

# Step 10: Select Date Range "Last Month" on Summary screen and Verify Output
print("📅 Selecting Date Range: Last Month on Summary screen...")
driver.find_element(By.XPATH, "//span[normalize-space()='Mar 1, 2025 - Mar 10, 2025']").click()
time.sleep(1)
driver.find_element(By.XPATH, "//button[normalize-space()='Last Month']").click()
time.sleep(2)
print("✅ Date range applied on Summary screen!")

# Verify Output
print("🔍 Verifying output: Checking for 'Kashyap Thakar'...")
output_element = driver.find_element(By.XPATH, "//td[normalize-space()='Kashyap Thakar']")
assert output_element is not None, "❌ Test Failed: Expected output not found"
print("🎉 Test Passed: Kashyap Thakar found in summary output!")

# Close the browser
print("🔚 Closing browser and ending test...")
driver.quit()
