# Everest Insights Module - Selenium Test Script 🏔️

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Setup WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
print("🚀 Starting Test: Everest Insights Module")

# Login to Everest
login_url = "https://qa.dashboard.everest.7span.in/#/login"
driver.get(login_url)
time.sleep(3)
print("🔑 Logging in...")

driver.find_element(By.XPATH, "//input[@id='email']").send_keys("kajal@7span.com")
driver.find_element(By.XPATH, "//input[@id='password']").send_keys("1")
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(3)
print("✅ Logged in successfully!")

# Navigate to Insights Module
driver.get("https://qa.dashboard.everest.7span.in/#/insights")
time.sleep(2)
print("📊 Navigating to Insights Module...")

# Navigate to Projects Billability Module and Open
driver.find_element(By.XPATH, "//span[@class='truncate'][normalize-space()='Projects']").click()
time.sleep(2)
print("📂 Opening Projects Billability...")

# Navigate to First Project and Open
project_element = driver.find_element(By.XPATH, "//table/tbody/tr/td[1]")
project_element.click()
time.sleep(3)
print("📁 Opening Project: NeuraBot...")

# Verify Milestones Billability Screen
assert "Milestones Billability" in driver.page_source
print("✅ Verified Milestones Billability Screen")

# Open Filter
driver.find_element(By.XPATH, "//span[contains(@class, 'inline-flex') and contains(@class, 'rounded-md')]//*[name()='svg']//*[name()='path' and contains(@fill, 'currentCol')][1]").click()
time.sleep(2)
print("🎛️ Opening Filter...")

# Click "Clear All" Button
driver.find_element(By.XPATH, "//button[normalize-space()='Clear All']").click()
time.sleep(2)
print("🧹 Clearing All Filters...")

# Close the Filter
driver.find_element(By.XPATH, "//span[@class='absolute -inset-2.5']").click()
time.sleep(2)
print("❌ Closing Filter...")

# Search Milestone Name
driver.find_element(By.XPATH, "//input[@id='search-input']").send_keys("Phase -1 ( Realism and Immersion )")
time.sleep(2)
assert "Phase -1 ( Realism and Immersion )" in driver.page_source
print("🔍 Searching for Milestone: Phase -1 ( Realism and Immersion )")

# Click Milestone to Open Details Page
driver.find_element(By.XPATH, "//tr[td[contains(text(), 'HoloTrain')]]").click()
time.sleep(3)
print("📑 Opening Milestone Details...")

# Scroll Down and Up
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)
print("📜 Scrolling Down and Up...")

# Navigate Back to Milestones Billability
driver.back()
time.sleep(3)
print("🔙 Going back to Milestones Billability...")

# Clear Search Bar
driver.find_element(By.XPATH, "//input[@id='search-input']").clear()
time.sleep(2)
print("📝 Clearing Search Bar...")

# Navigate to Employee Billability Module
driver.find_element(By.XPATH, "//span[contains(text(),'Employees')]").click()
time.sleep(3)
print("👥 Opening Employee Billability...")

# End Test
driver.quit()
print("🏁 Test Completed Successfully!")
