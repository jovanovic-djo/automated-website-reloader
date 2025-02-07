from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import argparse
from datetime import datetime
import random
import sys
from threading import Thread
from typing import List, Dict

class WebsiteRefresher:
    def __init__(self):
        self.drivers: Dict[str, webdriver.Chrome] = {}
        self.running = True

    def setup_driver(self) -> webdriver.Chrome:
        """Setup and return Chrome WebDriver with configured options"""
        chrome_options = Options()
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
            return None

    def refresh_single_website(self, url: str, interval: float, random_interval: bool = False, 
                             min_interval: float = None, max_interval: float = None):
        """Handle refreshing of a single website in its own thread"""
        driver = self.setup_driver()
        if not driver:
            return
        
        self.drivers[url] = driver
        refresh_count = 0
        
        try:
            print(f"Opening {url}...")
            driver.get(url)
            
            while self.running:
                try:
                    refresh_count += 1
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    driver.refresh()
                    print(f"[{current_time}] {url} - Refresh #{refresh_count} completed")
                    
                    # Calculate wait time
                    if random_interval and min_interval and max_interval:
                        wait_time = random.uniform(min_interval, max_interval)
                    else:
                        wait_time = interval
                    
                    time.sleep(wait_time)
                    
                except WebDriverException as e:
                    print(f"Error refreshing {url}: {e}")
                    print(f"Attempting to recover {url}...")
                    try:
                        driver.get(url)
                    except:
                        print(f"Failed to recover {url}. Restarting browser...")
                        driver.quit()
                        driver = self.setup_driver()
                        if driver:
                            self.drivers[url] = driver
                            driver.get(url)
                    continue
                
        except Exception as e:
            print(f"Thread error for {url}: {e}")
        
    def refresh_websites(self, urls: List[str], interval: float, random_interval: bool = False,
                        min_interval: float = None, max_interval: float = None):
        """Start refreshing multiple websites in parallel"""
        threads = []
        
        # Create and start a thread for each URL
        for url in urls:
            thread = Thread(target=self.refresh_single_website,
                          args=(url, interval, random_interval, min_interval, max_interval))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        try:
            # Keep the main thread running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping all refreshes...")
            self.running = False
            # Close all browsers
            for driver in self.drivers.values():
                try:
                    driver.quit()
                except:
                    pass
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Auto-refresh multiple websites using Chrome browser')
    parser.add_argument('urls', nargs='+', help='One or more website URLs to refresh')
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
    
    refresher = WebsiteRefresher()
    refresher.refresh_websites(args.urls, args.interval, args.random, args.min, args.max)

if __name__ == "__main__":
    main()