import requests
from bs4 import BeautifulSoup

# Function to fetch and parse the HTML content of a given URL
def fetch_and_parse(url):
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None
    
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return soup

# Function to extract product data from the parsed HTML
def extract_product_data(soup):
    # Extract relevant product details based on the assumed HTML structure
    # Modify these extraction methods based on your actual HTML structure.
    
    # Example of extracting data from the page
    # Modify these queries based on the HTML elements for your specific webpage
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
    # Loop through the data and compare
    for key in data1:
        value1 = data1[key]
        value2 = data2[key]
        print(f"\n{key}:")
        if value1 == value2:
            print(f"✅ Matched: {value1}")
        else:
            print(f"❌ Mismatch! URL 1: {value1} | URL 2: {value2}")

# Main function
def main():
    # URLs (You will update these as needed)
    first_url = "https://gothammeds.com/product/ogre-kush"
    second_url = "https://main.dbckn6x69ywtg.amplifyapp.com/product/ogre-kush"
    
    # Fetch and parse data from both URLs
    print(f"Fetching data from {first_url}...")
    soup1 = fetch_and_parse(first_url)
    
    print(f"Fetching data from {second_url}...")
    soup2 = fetch_and_parse(second_url)
    
    if soup1 and soup2:
        # Extract product data from both URLs
        data1 = extract_product_data(soup1)
        data2 = extract_product_data(soup2)
        
        # Compare the extracted data
        compare_data(data1, data2)

if __name__ == "__main__":
    main()
