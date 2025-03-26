import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def wait_for_element(xpath, timeout=10):
    """Wait for an element to be clickable and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

def login():
    """Logs in to the dashboard."""
    print("🔐 Login: Attempting to log in...")
    try:
        driver.get("https://qa.dashboard.everest.7span.in/#/login")
        wait_for_element("//input[@id='email']").send_keys("kajal@7span.com")
        wait_for_element("//input[@id='password']").send_keys("1" + Keys.RETURN)
        
        wait.until(EC.url_changes(driver.current_url))  # Wait for page redirection
        print("✅ Login: Success")
    except Exception as e:
        print(f"❌ Login: Failed - {e}")
        time.sleep(2)

def scroll_down(pixels = 700):
    """Scrolls down the page by a specified number of pixels."""
    try:
        driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(1)
        print(f"📜 Scrolled down by {pixels} pixels.")
    except Exception as e:
        print(f"❌ Failed to scroll, Error: {e}")

def scroll_to_element(xpath):
    """Scrolls the page until the specified element is in view."""
    try:
        # Wait until the element is present in the DOM
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # Scroll to the element smoothly
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        print(f"📜 Scrolled to element: {xpath}")
    except Exception as e:
        print(f"❌ Failed to scroll to element. Error: {e}")

def test_by_employee():
    """Tests the 'Timesheet By Employee' module in the Insights section."""
    try:
        driver.get("https://qa.dashboard.everest.7span.in/#/insights")
        time.sleep(2)

        # Click on 'By Employee' Module
        by_employee_module = wait_for_element("//span[contains(text(),'By Employee')]")
        by_employee_module.click()
        print("✅ Clicked on 'By Employee' Module")
        time.sleep(2)
        
        # Search for an employee
        search_bar = wait_for_element("//input[@id='search-Employee']")
        search_bar.send_keys("Krunal Baldha")
        time.sleep(2)
        
        # Click on the employee result
        search_result = wait_for_element("//div[contains(text(),'Krunal Baldha')]")
        search_result.click()
        print("✅ Selected Employee: Krunal Baldha")
        time.sleep(2)

        # Open the date selector dropdown
        date_selector = wait_for_element("//span[contains(text(),'-')]")
        date_selector.click()
        time.sleep(1)

        # Date filter XPaths
        date_filters = {
            "Today": "//button[normalize-space()='Today']",
            "Yesterday": "//button[normalize-space()='Yesterday']",
            "This Week": "//button[normalize-space()='This Week']",
            "Last Week": "//button[normalize-space()='Last Week']",
            "This Month": "//button[normalize-space()='This Month']",
            "Last Month": "//button[normalize-space()='Last Month']"
        }

        # Iterate through date filters
        for label, xpath in date_filters.items():
            print(f"🔄 Attempting to select {label}...")
            date_selector = wait_for_element("//span[contains(text(),'-')]")
            date_selector.click()
            time.sleep(1)
            try:
                date_option = wait_for_element(xpath)
                if date_option.is_displayed() and date_option.is_enabled():
                    date_option.click()
                    print(f"✅ Selected Date Filter: {label}")
                    time.sleep(2)
                else:
                    print(f"⚠️ {label} button is not interactable.")
            except Exception as e:
                print(f"❌ Failed to select {label}: {e}")

        search_bar.clear()
        print("✅ Cleared Search Input")
        print("✅ Test for 'By Employee' module completed successfully.")

    except Exception as e:
        print(f"❌ Test failed: {e}")
    time.sleep(2)

def test_by_team():
    """Tests the 'Timesheet By Team' module in the Insights section."""
    try:
        print("🔄 Navigating to 'Timesheet By Team' module...")
        driver.get("https://qa.dashboard.everest.7span.in/#/insights/timesheet/by-team")
        time.sleep(1)
        wait_for_element("//h1[normalize-space()='Timesheet By Team']")
        print("✅ Navigated to 'Timesheet By Team' Module")
        time.sleep(1)

        # Click Calendar to view team hours
        print("🕒 Clicking on Calendar day (4th)...")
        calendar = wait_for_element("//body//div//div[9]")
        calendar.click()
        time.sleep(2)

        # Scroll down to a specific element
        print("📜 Scrolling down to the team section...")
        scroll_to_element("//div[contains(@id, 'headlessui-dialog-panel')]")  # Adjusted XPath for dynamic id
        time.sleep(3)

        # Click on a specific team member’s hours box
        print("👤 Selecting a team member's hours...")
        team_hours_box = wait_for_element("//div[normalize-space()='Krunal Baldha']")
        team_hours_box.click()
        time.sleep(2)

        # Click on Employee name
        print("📌 Opening Employee details...")
        employee = wait_for_element("//div[normalize-space()='Krunal Baldha']")
        employee.click()
        time.sleep(2)

        print("✅ Test for 'Timesheet By Team' module completed successfully.")

    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    try:
        login()
        test_by_employee()
        test_by_team()
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
    finally:
        driver.quit()
        print("🚪 Browser Closed.")

if __name__ == "__main__":
    main()
