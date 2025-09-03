import os
import dotenv
import time
import json
import paramiko
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire import webdriver as wire_webdriver
from tabulate import tabulate  # For better table formatting

# Load environment variables
dotenv.load_dotenv()

# SSH and Database Credentials
SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT", 22))
SSH_USER = os.getenv("SSH_USER")
SSH_KEY_PATH = os.getenv("SSH_KEY_PATH")

DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DB")
DB_PORT = int(os.getenv("MYSQL_PORT", 3306))

# Ensure required environment variables exist
if not all([SSH_HOST, SSH_USER, SSH_KEY_PATH, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    print("❌ Missing environment variables in .env file!")
    exit()

# Establish SSH Tunnel
def create_ssh_tunnel():
    print("🔗 Establishing SSH Tunnel...")
    try:
        tunnel = SSHTunnelForwarder(
            (SSH_HOST, SSH_PORT),
            ssh_username=SSH_USER,
            ssh_pkey=SSH_KEY_PATH,
            remote_bind_address=(DB_HOST, DB_PORT)
        )
        tunnel.start()
        print("✅ SSH Tunnel Established!")
        return tunnel
    except Exception as e:
        print(f"❌ SSH Tunnel Error: {e}")
        exit()

# Launch Browser with Network Interceptor
def launch_browser():
    print("🚀 Launching Browser with Network Interceptor...")
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    driver = wire_webdriver.Chrome(options=options)
    return driver

# Perform Login
def login(driver):
    print("🔑 Logging in...")
    driver.get("https://qa.dashboard.everest.7span.in/#/login")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("krunal.b@7span.com")
    driver.find_element(By.ID, "password").send_keys("1")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Dashboard')]")))
    print("✅ Login Successful!")

# Capture Employee ID from API Response
def capture_employee_id(driver, employee_name):
    print(f"🔎 Searching for Employee: {employee_name}...")
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='search-Employee']")))
    search_input.clear()
    search_input.send_keys(employee_name)
    time.sleep(2)
    search_input.send_keys(Keys.ENTER)
    
    time.sleep(3)  # Allow API calls to complete
    for request in driver.requests:
        if "employees" in request.url and request.response:
            try:
                response_body = request.response.body.decode("utf-8")
                data = json.loads(response_body)
                for employee in data.get("employees", []):
                    if employee["name"] == employee_name:
                        print(f"✅ Employee ID Found: {employee['id']}")
                        return employee["id"]
            except Exception as e:
                print(f"⚠️ Error processing API response: {e}")
    
    print("❌ Employee ID Not Found!")
    return None

# Fetch Employee Data from Database
def fetch_employee_data(tunnel, employee_id, start_date, end_date):
    try:
        print("📡 Connecting to Database...")
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=tunnel.local_bind_port
        )
        cursor = connection.cursor(dictionary=True)

        query = f'''
            SELECT
                p.name AS project,
                SUM(t.planned_hours) AS total_planned_hours,
                SUM(CASE 
                        WHEN t.logged_by_employee = 1 THEN t.logged_hours 
                        ELSE 0 
                    END) AS employee_logged_hours,
                SUM(CASE 
                        WHEN t.logged_by_employee = 0 THEN t.logged_hours 
                        ELSE 0 
                    END) AS coordinator_logged_hours,
                SUM(t.billable_hours) AS total_billable_hours,
                SUM(t.non_billable_hours) AS total_non_billable_hours
            FROM
                timesheet t
                JOIN projects p ON t.project = p.id
            WHERE
                t.employee = '{employee_id}'
                AND t.date >= '{start_date}'
                AND t.date <= '{end_date}'
            GROUP BY
                p.name;
        '''
        
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        print("✅ Database Fetch Successful!")

        if result:
            print("\n📊 **Database Data:**")
            print(tabulate(result, headers="keys", tablefmt="grid"))  
        else:
            print("⚠️ No matching data found in the database!")

        return result

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return None

# Main Execution
def main():
    tunnel = create_ssh_tunnel()
    driver = launch_browser()
    try:
        login(driver)
        employee_name = "Krunal Baldha"
        employee_id = capture_employee_id(driver, employee_name)
        if employee_id:
            db_data = fetch_employee_data(tunnel, employee_id, "2025-03-01", "2025-03-24")
    finally:
        driver.quit()
        tunnel.stop()
        print("🛑 Browser & SSH Tunnel Closed.")

if __name__ == "__main__":
    main()
