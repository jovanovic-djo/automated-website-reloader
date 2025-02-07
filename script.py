from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import argparse
from datetime import datetime
import random
import sys

def setup_driver():
    """Setup and return Chrome WebDriver with configured options"""
    chrome_options = Options()
    # Uncomment the line below if you want to run in headless mode (no visible browser)
    # chrome_options.add_argument('--headless')
    
    # Add some common options to make browser more stable
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome WebDriver: {e}")
        print("Make sure you have Chrome and ChromeDriver installed.")
        sys.exit(1)

def refresh_website(url, interval, random_interval=False, min_interval=None, max_interval=None):
    """
    Open website in Chrome and continuously refresh it.
    
    Args:
        url (str): The website URL to refresh
        interval (int): Base interval in seconds between refreshes
        random_interval (bool): Whether to use random intervals
        min_interval (int): Minimum interval for random timing
        max_interval (int): Maximum interval for random timing
    """
    driver = setup_driver()
    refresh_count = 0
    
    try:
        print(f"Opening {url}...")
        driver.get(url)
        
        while True:
            try:
                refresh_count += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                driver.refresh()
                print(f"[{current_time}] Refresh #{refresh_count} completed")
                
                if random_interval and min_interval and max_interval:
                    wait_time = random.uniform(min_interval, max_interval)
                else:
                    wait_time = interval
                
                # Wait before next refresh
                time.sleep(wait_time)
                
            except WebDriverException as e:
                print(f"Error during refresh: {e}")
                print("Attempting to recover...")
                try:
                    driver.get(url)
                except:
                    print("Failed to recover. Restarting browser...")
                    driver.quit()
                    driver = setup_driver()
                    driver.get(url)
                continue
            
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    finally:
        print("Closing browser...")
        driver.quit()

def main():
    parser = argparse.ArgumentParser(description='Auto-refresh a website using Chrome browser')
    parser.add_argument('url', help='The website URL to refresh')
    parser.add_argument('-i', '--interval', type=float, default=60,
                        help='Interval between refreshes in seconds (default: 60)')
    parser.add_argument('-r', '--random', action='store_true',
                        help='Use random intervals between min and max values')
    parser.add_argument('--min', type=float,
                        help='Minimum interval for random timing (seconds)')
    parser.add_argument('--max', type=float,
                        help='Maximum interval for random timing (seconds)')
    
    args = parser.parse_args()
    
    if args.random and (args.min is None or args.max is None):
        parser.error("--random requires both --min and --max arguments")
    
    refresh_website(args.url, args.interval, args.random, args.min, args.max)

if __name__ == "__main__":
    main()