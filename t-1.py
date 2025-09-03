from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

company = "Flex Foods"
url = "https://money.rediff.com/gainers"

opts = Options()
opts.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=opts)

try:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#leftcontainer table tbody tr"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, "#leftcontainer table tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if company.lower() in cols[0].text.lower():
            print(f"Company      : {cols[0].text.strip()}")
            print(f"Group        : {cols[1].text.strip()}")
            print(f"Prev Close   : {cols[2].text.strip()}")
            print(f"Current Price: {cols[3].text.strip()}")
            print(f"% Change     : {cols[4].text.strip()}")
            break
    else:
        print(f"Company '{company}' not found.")

finally:
    driver.quit()
