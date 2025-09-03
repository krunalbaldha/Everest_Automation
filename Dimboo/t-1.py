from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# --- Configuration ---
URL = "https://zurolife.dev.dimboo.io/login/"
LOGIN_ID = "zuro.brand@dimboo.io"
PASSWORD = "7890"

# File paths (Update according to your PC)
IMAGE_PATH = r"C:\Automation\Selenium\Dimboo\Cill\123.jpg"
VIDEO_PATH = r"C:\Automation\Selenium\Dimboo\sample.mp4"
DOC_PATH = r"C:\Users\Krunal Baldha\Downloads\dummy_files\sample.pdf"

# --- XPaths ---
login_field = "//input[@name='email']"
password_field = "//input[@placeholder='******']"
company_dropdown_icon = "//div[@id='downshift-:r1:-toggle-button']"
zuro_studio_option = "//span[normalize-space()='ZURO STUDIO - Belgium']"
influencers_module = "//p[contains(text(),'Influencers')]"
campaign_management_xpath = "//p[contains(text(),'Campaign Management')]"
logout_btn = "//span[normalize-space()='Logout']"

# New XPaths
new_campaign_btn = "//button[normalize-space()='New Campaign']"
dropdown_icon = "//div[contains(@id,'downshift') and contains(@id,'toggle-button')]//span[@class='text-xl']//*[name()='svg']"
instagram_option = "//span[normalize-space()='instagram']"
save_file_btn = "//button[normalize-space()='Save file(s)']"
next_btn = "//button[normalize-space()='Next']"

campaign_image_icon = "//span[contains(@class,'relative flex h-full w-full items-center justify-center rounded object-cover text-7xl')]//*[name()='svg'][2]/*[name()='path'][1]"
campaign_title_field = "//input[@type='text']"
support_video_field = "//div[@class='h-screen w-full overflow-y-auto p-4 bg-app_bg_color']//div[3]//div[1]//div[1]//div[1]//div[1]"
support_doc_field = "//div[4]//div[1]//div[1]//div[1]//div[1]"

add_pos_btn = "//button[normalize-space()='Add PoS by filtering accounts']"
pos_selection = "//tbody/tr[3]/td[1]/input[1]"
save_pos_btn = "//button[normalize-space()='Save selection']"

campaign_desc_field = "//textarea[@id='description']"
add_milestone_btn = "//p[normalize-space()='New Milestone']"
milestone_title = "//input[@type='text'][1]"
milestone_desc = "//textarea[@id='description'][1]"
milestone_hashtags = "//textarea[@id='description'][2]"
milestone_support_video = "//div[@class='mt-3 space-y-4']//div[2]//div[1]//div[1]//div[1]//div[1]"
create_milestone_btn = "//button[normalize-space()='Create Milestone']"

launch_campaign_btn = "//button[normalize-space()='Launch Campaign']"

# --- Selenium Setup ---
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # Step 1: Open login page
    print("Opening login page... ")
    driver.get(URL)

    # Step 2: Login
    print("Entering login credentials...")
    wait.until(EC.presence_of_element_located((By.XPATH, login_field))).send_keys(LOGIN_ID)
    wait.until(EC.presence_of_element_located((By.XPATH, password_field))).send_keys(PASSWORD + Keys.RETURN)
    print("✅ Login submitted successfully.")

    # Step 3: Select Company from dropdown
    print("Waiting for overlay to disappear...")
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.backdrop-blur-sm")))
    except:
        print("⚠️ No overlay detected, continuing...")

    print("Selecting company: Zuro Studio...")
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, company_dropdown_icon)))
    driver.execute_script("arguments[0].click();", dropdown)
    wait.until(EC.element_to_be_clickable((By.XPATH, zuro_studio_option))).click()
    print("✅ Company selected successfully.")
    time.sleep(2)

    # Step 4: Navigate to Influencers → Campaign Management
    print("Navigating to Influencers Module...")
    wait.until(EC.element_to_be_clickable((By.XPATH, influencers_module))).click()
    print("✅ Influencers Module opened.")

    print("Opening Campaign Management...")
    wait.until(EC.element_to_be_clickable((By.XPATH, campaign_management_xpath))).click()
    print("✅ Campaign Management opened.")
    time.sleep(2)

    # Step 5: Click + New Campaign
    print("Clicking + New Campaign...")
    wait.until(EC.element_to_be_clickable((By.XPATH, new_campaign_btn))).click()

    # Step 6: Select Social Media (Instagram)
    print("Selecting Social Media type: Instagram...")
    # wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_icon))).click()
    # wait.until(EC.element_to_be_clickable((By.XPATH, instagram_option))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, next_btn))).click()

    # Step 7: Upload Campaign Image
    try:
        print("➡ Clicking + New Campaign...")
        campaign_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., '+ New Campaign')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", campaign_btn)
        campaign_btn.click()
        print("✅ Clicked + New Campaign")
    except Exception as e:
        print(f"❌ Campaign button click failed: {e}")

    try:
        print("➡ Uploading image...")
        upload_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='file']")
        ))
        upload_input.send_keys(r"C:\Automation\Selenium\Dimboo\Cill\123.jpg")
        print("✅ Image uploaded")
    except Exception as e:
        print(f"❌ Image upload failed: {e}")
        wait.until(EC.element_to_be_clickable((By.XPATH, save_file_btn))).click()

    # Step 8: Enter Campaign Title
    print("Entering Campaign Title...")
    wait.until(EC.presence_of_element_located((By.XPATH, campaign_title_field))).send_keys("Zuro Lifestyle - Influencer Campaign")

    # # Step 9–12: Upload Support Video & Doc
    # print("Uploading Support Video...")
    # try:
    #     print("📂 Uploading support video...")
    #     upload_input = wait.until(EC.presence_of_element_located((By.XPATH, support_video_field)))
    #     upload_input.send_keys(VIDEO_PATH)
    #     print("✅ Video uploaded successfully!")
    # except Exception as e:
    #     print(f"❌ Video upload failed: {e}")

    # print("Uploading Support Document...")
    # wait.until(EC.element_to_be_clickable((By.XPATH, support_doc_field))).click()
    # os.system(f'"{DOC_PATH}"')
    # time.sleep(2)

    # Step 13–14: Add POS
    try:
        print("➡ Waiting for overlay to disappear before clicking Add POS...")

        # Wait until overlay goes away
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'bg-black') and contains(@class,'opacity-50')]")
        ))

        # Now wait for button and click
        add_pos_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Add POS')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_pos_button)
        add_pos_button.click()

        print("✅ Add POS button clicked!")
    except Exception as e:
        print(f"❌ Failed to click Add POS: {e}")


    # Step 15–16: Campaign Dates (Skipping calendar picker automation for now)

    # Step 17: Enter Campaign Description
    print("Entering Campaign Description...")
    wait.until(EC.presence_of_element_located((By.XPATH, campaign_desc_field))).send_keys("This is a test influencer campaign created using Selenium.")

    # Step 18: Add New Milestone
    print("Adding New Milestone...")
    wait.until(EC.element_to_be_clickable((By.XPATH, add_milestone_btn))).click()

    print("Entering Milestone Title, Description, and Hashtags...")
    wait.until(EC.presence_of_element_located((By.XPATH, milestone_title))).send_keys("Milestone 1 - Awareness")
    wait.until(EC.presence_of_element_located((By.XPATH, milestone_desc))).send_keys("Influencers to post on Instagram Stories and Reels.")
    wait.until(EC.presence_of_element_located((By.XPATH, milestone_hashtags))).send_keys("#ZuroLifestyle #InfluencerCampaign")

    # Step 22–25: Upload Milestone Video & Doc
    print("Uploading Milestone Video...")
    wait.until(EC.element_to_be_clickable((By.XPATH, milestone_support_video))).click()
    os.system(f'"{VIDEO_PATH}"')
    time.sleep(2)

    print("Uploading Milestone Document...")
    wait.until(EC.element_to_be_clickable((By.XPATH, support_doc_field))).click()
    os.system(f'"{DOC_PATH}"')
    time.sleep(2)

    # Step 26: Create Milestone
    print("Creating Milestone...")
    wait.until(EC.element_to_be_clickable((By.XPATH, create_milestone_btn))).click()
    time.sleep(2)

    # Step 27: Launch Campaign
    print("Launching Campaign...")
    wait.until(EC.element_to_be_clickable((By.XPATH, launch_campaign_btn))).click()
    print("✅ Campaign launched successfully.")

    # Step 28: Logout
    print("Logging out...")
    wait.until(EC.element_to_be_clickable((By.XPATH, logout_btn))).click()
    print("✅ Logout successful.")

finally:
    print("Closing browser...")
    driver.quit()
    print("🎉 Test completed successfully!")
