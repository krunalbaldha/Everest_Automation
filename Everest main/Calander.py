import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the WebDriver (Ensure you have the appropriate WebDriver for your browser)
driver = webdriver.Chrome()

# Define the base URLs
login_url = "https://qa.dashboard.everest.7span.in/#/login"
performance_url = "https://qa.dashboard.everest.7span.in/#/performance"

# Define the credentials
username = "kajal@7span.com"
password = "1"

# Define the emoji options
emoji_paths = {
    "Never": "//span[contains(text(),'Never')]",
    "Rarely": "//span[contains(text(),'Rarely')]",
    "Sometimes": "//span[contains(text(),'Sometimes')]",
    "Often": "//span[contains(text(),'Often')]",
    "Usually": "//span[contains(text(),'Usually')]",
    "Almost Always": "//span[contains(text(),'Almost Always')]",
    "Gold Standard": "//span[contains(text(),'Gold Standard')]"
}

# Define the questions and expected answers
questions_answers = {
    "Teamwork": "Gold Standard",
    "Communication": "Rarely",
    "Giving and receiving feedback": "Sometimes",
    "Time management": "Often",
    "Analytical Thinking": "Usually",
    "Building work relationships": "Almost Always",
    "Quality and technical Skills": "Never",
    "Decision making": "Often",
    "Process thinking": "Gold Standard",
    "Mentoring": "Often",
    "Business Acumen & Strategy": "Almost Always"
}

# Function to log in
def login():
    driver.get(login_url)
    time.sleep(2)
    
    # Enter credentials and submit
    driver.find_element(By.XPATH, "//input[@id='email']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

# Function to navigate to Performance Module and open the dashboard
def open_performance_dashboard():
    driver.get(performance_url)
    time.sleep(2)
    
    # Navigate to Performance Module
    driver.find_element(By.XPATH, "//span[contains(text(),'Performance')]").click()
    time.sleep(2)
    
    # Navigate to the specific Quadrimester
    driver.find_element(By.XPATH, "//h3[contains(text(), 'FY 2024-25 - Quadrimester 3')]").click()
    time.sleep(2)
    
    # Open the performance dashboard
    driver.find_element(By.XPATH, "//h3[contains(text(), 'Kajal Pandya')]").click()
    time.sleep(2)
    
    # Click on the "Self Evaluation" button
    driver.find_element(By.XPATH, "//a[normalize-space()='Self Evaluation']").click()
    time.sleep(2)

# Function to fill out the self-evaluation
def fill_self_evaluation():
    # Iterate through the questions and select corresponding emojis
    for question, answer in questions_answers.items():
        # Find the question element
        question_element = driver.find_element(By.XPATH, f"//p[normalize-space()='{question}']")
        question_element.click()
        time.sleep(1)
        
        # Select the corresponding emoji
        emoji_xpath = emoji_paths[answer]
        driver.find_element(By.XPATH, emoji_xpath).click()
        time.sleep(1)
        
        # Click the "Next" button to move to the next question
        driver.find_element(By.XPATH, "//button[normalize-space()='Next']").click()
        time.sleep(2)

# Function to fill out the additional fields
def fill_additional_fields():
    # Fill out the Strengths field
    driver.find_element(By.XPATH, "//label[@for='strengths']").click()
    driver.find_element(By.XPATH, "//textarea[@id='strengths']").send_keys("Strengths response.")
    
    # Fill out the Areas for Improvement field
    driver.find_element(By.XPATH, "//label[@for='improvements']").click()
    driver.find_element(By.XPATH, "//textarea[@id='improvements']").send_keys("Areas for Improvement response.")
    
    # Fill out the Work Quality & Technical Skills field
    driver.find_element(By.XPATH, "//label[@for='workQuality']").click()
    driver.find_element(By.XPATH, "//textarea[@id='workQuality']").send_keys("Work Quality & Technical Skills response.")

# Function to submit the form
def submit_form():
    # Click the Submit button
    driver.find_element(By.XPATH, "//button[normalize-space()='Submit']").click()
    time.sleep(2)

# Main execution
def main():
    login()
    open_performance_dashboard()
    fill_self_evaluation()
    fill_additional_fields()
    submit_form()
    
    # Close the driver after completion
    driver.quit()

if __name__ == "__main__":
    main()
