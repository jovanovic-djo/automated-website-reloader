from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create():
    driver = Options()
    driver.add_argument('--no-sandbox')
    driver.add_argument('--disable-dev-shm-usage')
    driver.add_argument('--disable-gpu')
    driver.add_argument('--headless')

    try:
        driver = webdriver.Chrome(options=driver)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome WebDriver: {e}")
        return None
