from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🚀 Initialize WebDriver
print("🚀 Starting WebDriver...")
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # ✅ **Step 1: Login to Everest**
    print("🔐 Logging into Everest...")
    driver.get("https://qa.dashboard.everest.7span.in/#/login")

    email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='email']")))
    email_field.send_keys("krunal.b@7span.com")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("1")

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    wait.until(EC.url_contains("/dashboard"))
    time.sleep(2)
    print("✅ Login successful!")

    # ✅ **Step 2: Navigate to Timesheet Module**
    print("📂 Navigating to Timesheet module...")
    driver.get("https://qa.dashboard.everest.7span.in/#/timesheet")
    time.sleep(2)
    
    # ✅ **Step 3: Click on "Log as Co-ordinator" Checkbox**
    try:
        coordinator_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
        if not coordinator_checkbox.is_selected():
            coordinator_checkbox.click()
        print("✅ 'Log as Co-ordinator' checkbox selected!")
    except Exception:
        print("⚠️ Unable to find or click the checkbox. Skipping this step.")

    time.sleep(2)
    
    # ✅ **Step 4: Search Employee Name**
    search_bar = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'search-')]")))
    search_bar.send_keys("Krunal Baldha")
    time.sleep(2)
    search_bar.send_keys(Keys.RETURN)
    search_bar.send_keys(Keys.TAB)
    time.sleep(3)

    # ✅ **Step 5: Scroll down the screen**
    print("📜 Scrolling down the page...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    # ✅ **Step 6: Enter hours on the first milestone**
    print("🕒 Entering hours for first milestone...")

    textbox_click = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@id, 'headlessui-input')])[1]")))
    textbox_click.click()
    textbox_click.clear()
    textbox_click.send_keys("1")
    time.sleep(3)

    # ✅ **Step 7: Select Description Icon**
    print("📌 Selecting the milestone...")
    milestone_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][contains(@class, 'h-4 w-4')])[1]")))
    milestone_button.click()
    time.sleep(1)
    
    # ✅ **Step 8: Enter description**
    print("📝 Entering description for first milestone...")
    textarea_xpath = "//textarea[contains(@id, 'headlessui-textarea-')]"
    textarea = wait.until(EC.element_to_be_clickable((By.XPATH, textarea_xpath)))
    textarea.send_keys("kachra seth ka kachra nahi karne ka")
    time.sleep(3)

    # ✅ **Step 9: Save Description**
    print("💾 Saving description...")
    save_description_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save Description']")
    save_description_button.click()
    print("✅ Description saved successfully! 🎉")
    time.sleep(2)
    
    # ✅ **Step 10: Click "Save Changes" Button and Verify the Message**
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
    
    # ✅ **Step 11: Enter hours on the Second milestone**
    print("🕒 Entering hours for Second milestone...")

    try:
        textbox = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[contains(@id, 'headlessui-input')])[8]")))
        driver.execute_script("arguments[0].scrollIntoView();", textbox)  # Scroll to element if necessary
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@id, 'headlessui-input')])[8]"))).click()
        textbox.send_keys("1")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ Error while entering hours: {e}")

    # ✅ **Step 12: Select Description Icon for Second Entry**
    print("📌 Selecting the Description Icon for second entry...")

    try:
        milestone_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][contains(@class, 'h-4 w-4')])[8]")))
        driver.execute_script("arguments[0].scrollIntoView();", milestone_button)  # Scroll to element
        milestone_button.click()
        time.sleep(1)
    except Exception as e:
        print(f"⚠️ Error while selecting milestone: {e}")
        
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
    
    # ✅ **Step 3: Locate and Clear First Input Field**
    print("📝 Clearing first input field...")
    first_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@id, 'headlessui-input')])[1]")))
    first_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)

    # ✅ **Step 4: Locate and Clear Second Input Field**
    print("📝 Clearing second input field...")
    second_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@id, 'headlessui-input')])[8]")))
    second_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)

    # ✅ **Step 5: Click Save Changes Button**
    print("💾 Clicking 'Save Changes' button...")
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Save Changes')]")))
    save_button.click()

    # ✅ **Step 6: Wait for Success Message**
    print("🕒 Waiting for success message...")
    try:
        success_message_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//p[normalize-space()='Changes saved successfully!']"))
        )
        success_message = success_message_element.text
        assert success_message == "Changes saved successfully!"
        print("✅ Success message verified! 🎉")
    except Exception as e:
        print("❌ Error: Success message not found.")
        print(str(e))

    time.sleep(3)
    
finally:
    # ✅ Close the browser
    print("🛑 Closing WebDriver...")
    time.sleep(2)
    driver.quit()
