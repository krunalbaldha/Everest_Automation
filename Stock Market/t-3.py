import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata

# ------------------ SETTINGS ------------------
URL = "https://money.rediff.com/gainers"
COMPANY = "Otco Internation"
STRICT_EXACT_MATCH = True
TOLERANCE_PCT = 0.05
EXCEL_FILE = "stock_history.xlsx"

# ------------------ UTILITIES ------------------
def clean_num(txt: str) -> float:
    if not txt:
        raise ValueError("Empty numeric text")
    t = unicodedata.normalize("NFKC", txt)
    t = t.replace("%", "").replace("+", "").replace(",", "").strip()
    return float(t)

def nearly_equal(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol

# ------------------ DRIVER SETUP ------------------
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(), options=chrome_options)

try:
    driver.get(URL)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='dataTable']//tbody//tr"))
    )

    # 1️⃣ Find company link
    if STRICT_EXACT_MATCH:
        xpath = f"//a[normalize-space()='{COMPANY}']"
    else:
        xpath = f"//a[contains(normalize-space(), '{COMPANY.strip()}')]"

    link_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    # 2️⃣ Get entire row in one go
    row_cells = link_elem.find_elements(By.XPATH, "./ancestor::tr/td")

    # 3️⃣ Extract data directly
    group_txt       = row_cells[1].text
    prev_close      = clean_num(row_cells[2].text)
    current_price   = clean_num(row_cells[3].text)
    change_pct      = clean_num(row_cells[4].text)
    computed_pct    = ((current_price - prev_close) / prev_close) * 100.0

    if not nearly_equal(computed_pct, change_pct, TOLERANCE_PCT):
        raise AssertionError(
            f"Validation failed: page %Change={change_pct:.4f}, computed={computed_pct:.4f}"
        )

    print(f"Company       : {link_elem.text.strip()}")
    print(f"Group         : {group_txt.strip()}")
    print(f"Prev Close    : {prev_close}")
    print(f"Current Price : {current_price}")
    print(f"% Change      : {change_pct}  (validated ✓)")

    # 4️⃣ Save to Excel (add as new column for each run)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE, index_col=0)
        if COMPANY not in df.index:
            df.loc[COMPANY] = [None] * len(df.columns)
    else:
        df = pd.DataFrame(index=[COMPANY])

    df[timestamp] = None
    df.at[COMPANY, timestamp] = current_price
    df.to_excel(EXCEL_FILE)

    print(f"Data saved to '{EXCEL_FILE}' with timestamp: {timestamp}")

finally:
    driver.quit()
