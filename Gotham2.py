import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Function to fetch and parse data from a WordPress-based site (static content)
def fetch_and_parse_wordpress(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to fetch and parse data from a React/Node.js-based site (dynamic content)
def fetch_and_parse_react(url):
    # Selenium WebDriver setup
    options = Options()
    options.headless = True  # Run in headless mode (no browser UI)
    
    # Set up WebDriver for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Open the React/Node.js URL
    driver.get(url)
    time.sleep(5)  # Give the page time to load
    
    # Fetch the page source after JavaScript rendering
    page_source = driver.page_source
    driver.quit()
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

# Function to extract product data from the parsed HTML (common for both websites)
def extract_product_data(soup):
    product_data = {
        "Pro Breadcrumb": soup.find('nav', class_='breadcrumb').get_text(strip=True) if soup.find('nav', class_='breadcrumb') else "Not Found",
        "Pro Title": soup.find('h1', class_='product-title').get_text(strip=True) if soup.find('h1', class_='product-title') else "Not Found",
        "Pro Description": soup.find('div', class_='product-description').get_text(strip=True) if soup.find('div', class_='product-description') else "Not Found",
        "Pro Image": soup.find('img', class_='product-image')['src'] if soup.find('img', class_='product-image') else "Not Found",
        "Pro Gallery": soup.find('div', class_='product-gallery').get_text(strip=True) if soup.find('div', class_='product-gallery') else "Not Found",
        "Pro Price": soup.find('span', class_='product-price').get_text(strip=True) if soup.find('span', class_='product-price') else "Not Found",
        "Pro Variation": soup.find('select', class_='product-variation').get_text(strip=True) if soup.find('select', class_='product-variation') else "Not Found",
        "Pro Stock": soup.find('span', class_='product-stock').get_text(strip=True) if soup.find('span', class_='product-stock') else "Not Found"
    }
    return product_data

# Function to compare the product data from two different URLs
def compare_data(data1, data2):
    for key in data1:
        value1 = data1[key]
        value2 = data2[key]
        print(f"\n{key}:")
        if value1 == value2:
            print(f"✅ Matched: {value1}")
        else:
            print(f"❌ Mismatch! URL 1: {value1} | URL 2: {value2}")

# Function to display fetched data for both URLs
def display_fetched_data(data, url):
    print(f"\nData from {url}:\n")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("\n" + "-"*50 + "\n")

# Main function
def main():
    # URLs (you will update these as needed)
    first_url = "https://gothammeds.com/product/ogre-kush"  # WordPress URL
    second_url = "https://main.dbckn6x69ywtg.amplifyapp.com/product/ogre-kush"  # React/Node.js URL
    
    # Fetch and parse data from WordPress (static content)
    print(f"Fetching data from {first_url}...\n")
    soup1 = fetch_and_parse_wordpress(first_url)
    
    # Fetch and parse data from React/Node.js (dynamic content)
    print(f"Fetching data from {second_url}...\n")
    soup2 = fetch_and_parse_react(second_url)
    
    if soup1 and soup2:
        # Extract product data from both URLs
        data1 = extract_product_data(soup1)
        data2 = extract_product_data(soup2)
        
        # Display fetched data for both URLs
        display_fetched_data(data1, first_url)
        display_fetched_data(data2, second_url)
        
        # Compare the extracted data
        compare_data(data1, data2)

if __name__ == "__main__":
    main()
