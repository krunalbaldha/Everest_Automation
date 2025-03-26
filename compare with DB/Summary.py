import sshtunnel
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configurations
SSH_CONFIG = {
    "host": "3.108.183.243",
    "port": 22,
    "user": "forge",
    "key_path": "C:/Users/Krunal Baldha/.ssh/id_rsa"
}

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "forge",
    "password": "rY3fFiM3vaEBLXfUdLkT",
    "database": "everest_qa",
    "port": 3306
}

DATE_RANGE = {"start": "2025-03-01", "end": "2025-03-24"}

print("🔍 Starting Database & UI Data Verification")

# Establish SSH Tunnel
try:
    print("🚀 Establishing SSH Connection...")
    tunnel = sshtunnel.SSHTunnelForwarder(
        (SSH_CONFIG["host"], SSH_CONFIG["port"]),
        ssh_username=SSH_CONFIG["user"],
        ssh_pkey=SSH_CONFIG["key_path"],
        remote_bind_address=("127.0.0.1", DB_CONFIG["port"]),
    )
    tunnel.start()
    print("✅ SSH Connection Successful!")

    print("🔄 Connecting to MySQL Database...")
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=tunnel.local_bind_port,
    )
    cursor = db_connection.cursor(dictionary=True)

    print("📥 Fetching Data from Database...")
    query = """
        SELECT
            CONCAT(du.first_name, ' ', du.last_name) AS name,
            SUM(t.logged_hours) AS logged_hours,
            SUM(t.billable_hours) AS billable_hours,
            SUM(t.non_billable_hours) AS non_billable_hours,
            SUM(t.logged_hours - (t.billable_hours + t.non_billable_hours)) AS not_reviewed_hours,
            du.date_reviewed AS coordinator_date_reviewed
        FROM timesheet t
        JOIN projects p ON t.project = p.id
        JOIN milestones m ON t.milestone = m.id
        JOIN directus_users du ON m.co_ordinator = du.id
        WHERE t.date BETWEEN %s AND %s
        AND t.logged_hours != (t.billable_hours + t.non_billable_hours)
        GROUP BY du.id
        ORDER BY not_reviewed_hours DESC;
    """

    cursor.execute(query, (f"{DATE_RANGE['start']} 00:00:00", f"{DATE_RANGE['end']} 23:59:59"))
    db_results = cursor.fetchall()

    # ✅ Displaying DB results
    print(f"\n✅ Data fetched from DB ({len(db_results)} records):")
    for record in db_results:
        print(f"   🤵 Name: {record['name']}, Logged: {record['logged_hours']}, "
              f"Billable: {record['billable_hours']}, Non-Billable: {record['non_billable_hours']}, "
              f"Unreviewed: {record['not_reviewed_hours']}, Last Reviewed: {record['coordinator_date_reviewed']}")

    # Close database connection
    cursor.close()
    db_connection.close()

    # Start Web Scraping
    print("\n🌐 Launching Selenium WebDriver...")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("https://qa.dashboard.everest.7span.in/#/login")
    time.sleep(2)

    print("🔑 Logging in...")
    driver.find_element(By.ID, "email").send_keys("krunal.b@7span.com")
    driver.find_element(By.ID, "password").send_keys("1")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    print("📊 Navigating to Insights > Summary...")
    driver.find_element(By.XPATH, "//span[contains(text(),'Insights')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//span[contains(text(),'Summary')]").click()
    time.sleep(3)

    print("📋 Extracting UI Data...")
    ui_results = []
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    for row in rows:
        name = row.find_element(By.XPATH, "./td[1]").text.strip()
        hours = row.find_element(By.XPATH, "./td[2]").text.strip()
        last_reviewed = row.find_element(By.XPATH, "./td[3]").text.strip()
        ui_results.append({
            "name": name,
            "not_reviewed_hours": hours,
            "last_reviewed": last_reviewed
        })

    driver.quit()
    print(f"✅ Data fetched from UI ({len(ui_results)} records)")
    print("🔎 Comparing Database Data with UI Data...")

    # Compare DB vs UI
    for db_entry in db_results:
        match = next((ui for ui in ui_results if ui["name"] == db_entry["name"]), None)

        if match:
            print(f"🔄 Comparing {db_entry['name']}...")

            # Convert 'not_reviewed_hours' to integers before comparison
            db_hours = int(float(db_entry['not_reviewed_hours'])) if db_entry['not_reviewed_hours'] else 0
            ui_hours = int(match['not_reviewed_hours']) if match['not_reviewed_hours'].isdigit() else 0

            if db_hours == ui_hours:
                print(f"✅ Match in Unreviewed Hours: {db_entry['name']} - DB={db_hours} UI={ui_hours}")
            else:
                print(f"❌ Mismatch in Unreviewed Hours: {db_entry['name']} - DB={db_hours} UI={ui_hours}")

        else:
            print(f"❌ Name {db_entry['name']} not found in UI")

    # Stop SSH tunnel
    tunnel.stop()
    print("✅ Verification Completed Successfully!")

except Exception as e:
    print(f"❌ An error occurred: {str(e)}")
