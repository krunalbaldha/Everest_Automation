from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import math
import time
import unicodedata

# ------------------ SETTINGS ------------------
URL = "https://money.rediff.com/gainers"     
COMPANY = "Otco Internation"                      
STRICT_EXACT_MATCH = True                    
TOLERANCE_PCT = 0.05                         

# ------------------ UTILITIES ------------------
def clean_num(txt: str) -> float:
    """Convert '2,756.95', '+ 7.73', '  148.20' to float safely."""
    if txt is None:
        raise ValueError("Empty numeric text")
    # Normalize unicode (handles NBSP etc.)
    t = unicodedata.normalize("NFKC", txt)
    # Remove percent sign, plus sign, commas and stray spaces
    t = t.replace("%", "").replace("+", "").replace(",", "").strip()
    # Some pages use non-breaking space; ensure removal
    t = t.replace("\u00a0", "").strip()
    return float(t)

def nearly_equal(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol

# ------------------ DRIVER SETUP ------------------
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(), options=chrome_options)

try:
    driver.get(URL)

    # Wait for at least one “gainer” row to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#leftcontainer table tbody tr"))
    )

    # Try exact match first (most reliable)
    target_link_xpath = f"//table//tbody//tr//td[1]//a[normalize-space()='{COMPANY}']"

    link_elem = None
    if STRICT_EXACT_MATCH:
        try:
            link_elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, target_link_xpath))
            )
        except Exception:
            link_elem = None

    # Fallback: partial match (if company text is truncated on page)
    if link_elem is None:
        alt_xpath = f"//table//tbody//tr//td[1]//a[contains(normalize-space(), '{COMPANY.strip()}')]"
        link_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, alt_xpath))
        )

    # Get the row (tr) for the company
    row = link_elem.find_element(By.XPATH, "./ancestor::tr")

    # Column mapping on Rediff Gainers: [1]=Company, [2]=Group, [3]=Prev Close, [4]=Current Price, [5]=% Change
    group_txt        = row.find_element(By.XPATH, "./td[2]").text
    prev_close_txt   = row.find_element(By.XPATH, "./td[3]").text
    current_price_txt= row.find_element(By.XPATH, "./td[4]").text
    change_pct_txt   = row.find_element(By.XPATH, "./td[5]").text

    # Clean + parse numbers
    prev_close   = clean_num(prev_close_txt)
    current_price= clean_num(current_price_txt)
    change_pct   = clean_num(change_pct_txt)

    # Sanity validation: recompute % change from prices
    computed_pct = ((current_price - prev_close) / prev_close) * 100.0
    if not nearly_equal(computed_pct, change_pct, TOLERANCE_PCT):
        # Try a very small refresh once if values just updated
        driver.refresh()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#leftcontainer table tbody tr"))
        )
        # Re-locate row and re-read (exact same steps)
        if STRICT_EXACT_MATCH:
            try:
                link_elem = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, target_link_xpath))
                )
            except Exception:
                link_elem = None
        if link_elem is None:
            alt_xpath = f"//table//tbody//tr//td[1]//a[contains(normalize-space(), '{COMPANY.strip()}')]"
            link_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, alt_xpath))
            )
        row = link_elem.find_element(By.XPATH, "./ancestor::tr")
        group_txt        = row.find_element(By.XPATH, "./td[2]").text
        prev_close_txt   = row.find_element(By.XPATH, "./td[3]").text
        current_price_txt= row.find_element(By.XPATH, "./td[4]").text
        change_pct_txt   = row.find_element(By.XPATH, "./td[5]").text
        prev_close   = clean_num(prev_close_txt)
        current_price= clean_num(current_price_txt)
        change_pct   = clean_num(change_pct_txt)
        computed_pct = ((current_price - prev_close) / prev_close) * 100.0

    # Final strict assertion (no silent wrong data)
    if not nearly_equal(computed_pct, change_pct, TOLERANCE_PCT):
        raise AssertionError(
            f"Validation failed: page %Change={change_pct:.4f}, computed={computed_pct:.4f}"
        )

    # OUTPUT (accurate, validated)
    print(f"Company       : {link_elem.text.strip()}")
    print(f"Group         : {group_txt.strip()}")
    print(f"Prev Close    : {prev_close}")
    print(f"Current Price : {current_price}")
    print(f"% Change      : {change_pct}  (validated ✓)")

finally:
    driver.quit()
