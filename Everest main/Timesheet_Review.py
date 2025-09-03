from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# URLs
login_url = "https://qa.dashboard.everest.7span.in/#/login"
timesheet_url = "https://qa.dashboard.everest.7span.in/#/timesheet"

driver.get(login_url)

# Wait for Login Elements
wait = WebDriverWait(driver, 10)
email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
password_input = driver.find_element(By.ID, "password")
signin_button = driver.find_element(By.XPATH, "//button[@type='submit']")
time.sleep(2)

# Perform Login
time.sleep(1)
email_input.send_keys("krunal.b@7span.com")
password_input.send_keys("1")
signin_button.click()

# Wait for Timesheet Page Load
time.sleep(2)
driver.get(timesheet_url)
time.sleep(3)

# Click Review Button with Dynamic ID Handling
review_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'radix-') and contains(@id, '-trigger-review')]")))
time.sleep(2)
review_button.click()
time.sleep(2)

# Project Search
project_search = wait.until(EC.presence_of_element_located((By.ID, "search-Project")))
project_search.send_keys("TaskMind AI")
time.sleep(2)
project_search.send_keys(Keys.RETURN)
time.sleep(2)

# Milestone Search
milestone_search = wait.until(EC.presence_of_element_located((By.ID, "search-Milestone")))
milestone_search.send_keys("tms - Front-End UI Implementation")
time.sleep(2)
milestone_search.send_keys(Keys.RETURN)
time.sleep(2)

# New Review Scenario: Approving and Disapproving Employee Hours

def review_employee_hours(approve_percentage):
    # Navigate to First Review Box and Open Description
    description_icon = wait.until(EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@class='h-4 w-4 false'])[1]")))
    description_icon.click()
    time.sleep(2)
    
    description_area = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@id, 'headlessui-textarea-')]")))
    description_area.click()
    time.sleep(2)
    
    # Verify Employee Name
    employee_names = ["Mit Makwana", "Krunal Baldha"]
    for name in employee_names:
        employee_element = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[normalize-space()='{name}']")))
        assert employee_element is not None, f"Employee {name} not found!"
    
    # Locate Input Boxes for Approval
    log_hours_input = driver.find_element(By.XPATH, "//input[contains(@id, 'headlessui-input')][following-sibling::div[contains(@class, 'bg-white')]]")
    approved_hours_input = driver.find_element(By.XPATH, "//input[contains(@id, 'headlessui-input')][following-sibling::div[contains(@class, 'bg-green')]]")
    unapproved_hours_input = driver.find_element(By.XPATH, "//input[contains(@id, 'headlessui-input')][following-sibling::div[contains(@class, 'bg-red')]]")
    
    # Get Employee Logged Hours
    logged_hours = int(log_hours_input.get_attribute("value"))
    approve_hours = int(logged_hours * approve_percentage / 100)
    unapprove_hours = logged_hours - approve_hours
    
    # Enter Approved Hours
    approved_hours_input.clear()
    approved_hours_input.send_keys(str(approve_hours))
    time.sleep(2)
    
    # Enter Unapproved Hours
    unapproved_hours_input.clear()
    unapproved_hours_input.send_keys(str(unapprove_hours))
    time.sleep(2)
    
    # Click Save Changes
    save_button = driver.find_element(By.XPATH, "//button[text()='Save Change']")
    save_button.click()
    time.sleep(2)
    
    # Verify Success Message
    success_message = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Changes saved successfully')]")))
    assert success_message is not None, "Success message not displayed!"

# Scenario 1: Approve 100% of Employee Hours
review_employee_hours(100)
time.sleep(2)

# Scenario 2: Approve 50% and Unapprove 50% of Employee Hours
review_employee_hours(50)
time.sleep(2)

# Close Browser
driver.quit()
