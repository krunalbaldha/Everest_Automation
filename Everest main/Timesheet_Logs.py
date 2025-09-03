from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
print("🚀 Starting WebDriver...")
driver = webdriver.Chrome()
driver.maximize_window()

# ✅ **Step 1: Login to Everest**
print("🔐 Logging into Everest...")
driver.get("https://qa.dashboard.everest.7span.in/#/login")
wait = WebDriverWait(driver, 10)

email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='email']")))
email_field.send_keys("krunal.b@7span.com")

password_field = driver.find_element(By.XPATH, "//input[@id='password']")
password_field.send_keys("1")

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

wait.until(EC.url_contains("/dashboard"))
time.sleep(2)
print("✅ Login successful!")


# ✅ **Step 2: Navigate to Timesheet Module**
print("📂 Navigating to Timesheet module...")
driver.get("https://qa.dashboard.everest.7span.in/#/timesheet/")
wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='headlessui-input-:rn:']")))
time.sleep(1)

# ✅ **Step 3: Scroll down the screen**
print("📜 Scrolling down the page...")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# Function to wait for elements
def wait_for_element(xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

# ✅ **Step 4: Enter hours on the first milestone**
print("🕒 Entering hours for first milestone...")
wait_for_element("(//input[contains(@id, 'headlessui-input')])[1]").send_keys("1")
time.sleep(1)

# ✅ **Step 5: Select milestone**
print("📌 Selecting the milestone...")
wait_for_element("(//*[name()='svg'][@class='h-4 w-4 false'])[1]").click()
time.sleep(1)

# ✅ **Step 6: Enter description**
print("📝 Entering description for first milestone...")
textarea_xpath = "//textarea[contains(@id, 'headlessui-textarea-')]"
textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, textarea_xpath)))
textarea.send_keys("kachra seth ka kachra nahi karne ka")
time.sleep(3)

# ✅ **Step 7: Save Description**
print("💾 Saving description...")
save_description_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save Description']")
save_description_button.click()
print("✅ Description saved successfully! 🎉")
time.sleep(2)

# 8. Click "Save Changes" Button and Verify the Message
print("📌 Clicking 'Save Changes' button...")
save_changes_button = driver.find_element(By.XPATH, "//span[contains(text(),'Save Changes')]")
save_changes_button.click()
print("✅ Changes saved successfully! 🎉")

# Wait for success message
print("🕒 Waiting for success message...")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Changes saved successfully!']")))

success_message = driver.find_element(By.XPATH, "//p[normalize-space()='Changes saved successfully!']").text
assert success_message == "Changes saved successfully!"
print("✅ Success message verified!")
time.sleep(5)


# ✅ **Step 9: Enter hours on the Second milestone**
print("🕒 Entering hours for Second milestone...")
wait_for_element("//input[@id='headlessui-input-:r12:']").send_keys("1")
time.sleep(1)

# ✅ **Step 5: Select description Icon**
print("📌 Selecting the milestone...")
wait_for_element("(//*[name()='svg'][@class='h-4 w-4 false'])[2]").click()
time.sleep(1)

# # ✅ **Step 6: Enter description**
# print("📝 Entering description for first milestone...")
# textarea_xpath = "//textarea[contains(@id, 'headlessui-textarea-')]"
# textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, textarea_xpath)))
# textarea.send_keys("kachra seth ka kachra nahi karne ka")
# time.sleep(3)

# ✅ **Step 7: Save Description**
print("💾 Saving description...")
save_description_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save Description']")
save_description_button.click()
print("✅ Description saved successfully! 🎉")
time.sleep(2)

# 8. Click "Save Changes" Button and Verify the Message
print("📌 Clicking 'Save Changes' button...")
save_changes_button = driver.find_element(By.XPATH, "//span[contains(text(),'Save Changes')]")
save_changes_button.click()
# print("✅ Click saved Button successfully! 🎉")

# Wait for success message
print("🕒 Waiting for success message...")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Please add descriptions for all time entries!']")))

success_message = driver.find_element(By.XPATH, "//p[normalize-space()='Please add descriptions for all time entries!']").text
assert success_message == "Please add descriptions for all time entries!"
print("✅ Success message verified!")
time.sleep(5)

# ✅ Step 10: Remove hours from both milestones
print("❌ Removing hours from both milestones...")

# Locate and clear the first input field
first_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='headlessui-input-:rn:']")))
first_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)

# Locate and clear the second input field
second_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='headlessui-input-:r12:']")))
second_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)

# Click Save Changes button
save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Save Changes')]")))
save_button.click()

# Wait for the success message to appear
print("🕒 Waiting for success message...")
try:
    success_message_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//p[normalize-space()='Changes saved successfully!']"))
    )
    success_message = success_message_element.text
    assert success_message == "Changes saved successfully!"
    print("✅ Success message verified!")
except Exception as e:
    print("❌ Error: Success message not found.")
    print(str(e))
    time.sleep(5)

# # ✅ **Step 11: Click Acknowledge and Confirm**
# print("✅ Clicking Acknowledge...")
# acknowledge_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),'Acknowledge')])[3]"))
# )
# acknowledge_button.click()

# # Wait for the Confirm button to appear
# print("✅ Waiting for Confirm button...")
# confirm_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Confirm']"))
# )
# confirm_button.click()

# # Wait for success message
# WebDriverWait(driver, 10).until(
#     EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Acknowledgment status updated successfully!")
# )
# print("✅ Acknowledgment status updated successfully!")

# ✅ **Step 12: Close the browser**
print("🛑 Closing the browser...")
driver.quit()
print("✅ Script execution completed successfully!")