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

URL = "https://money.rediff.com/gainers"
COMPANY = "Polo Queen Industria"
STRICT_EXACT_MATCH = True
TOLERANCE_PCT = 0.05
EXCEL_FILE = "stock_history.xlsx"

def clean_num(txt: str) -> float:
    if not txt:
        raise ValueError("Empty numeric text")
    t = unicodedata.normalize("NFKC", txt)
    t = t.replace("%", "").replace("+", "").replace(",", "").strip()
    return float(t)

def nearly_equal(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(), options=chrome_options)

try:
    driver.get(URL)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='dataTable']"))
    )

    if STRICT_EXACT_MATCH:
        xpath = f"//a[normalize-space()='{COMPANY}']"
    else:
        xpath = f"//a[contains(normalize-space(), '{COMPANY.strip()}')]"

    link_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    row_cells = link_elem.find_elements(By.XPATH, "./ancestor::tr/td")

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
    # print(f"Group         : {group_txt.strip()}")
    print(f"Prev Close    : {prev_close}")
    print(f"Current Price : {current_price:.2f}")
    # print(f"% Change      : {change_pct}  (validated ✓)")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    new_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Company": COMPANY,
        "Group": group_txt.strip(),
        "Prev Close": prev_close,
        "Current Price": f"{current_price:.2f}",
        "% Change": change_pct
    }])

    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_excel(EXCEL_FILE, index=False)
    print(f"Data appended to '{EXCEL_FILE}' with timestamp: {timestamp}")

finally:
    driver.quit()
