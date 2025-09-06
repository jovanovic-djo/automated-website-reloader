# script.py
import os
import time
import random
import sys
from threading import Thread
from datetime import datetime
from typing import List, Dict
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
from driver_manager import create

class WebsiteRefresher:
    def __init__(self):
        self.drivers: Dict[str, object] = {}
        self.running = True

    def refresh_single_website(self, url: str, interval: float, random_interval: bool = False, 
                             min_interval: float = None, max_interval: float = None):
        driver = create()
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
                        driver = create()
                        if driver:
                            self.drivers[url] = driver
                            driver.get(url)
                    continue
        except Exception as e:
            print(f"Thread error for {url}: {e}")

    def refresh_websites(self, urls: List[str], interval: float, random_interval: bool = False,
                        min_interval: float = None, max_interval: float = None):
        threads = []
        for url in urls:
            thread = Thread(target=self.refresh_single_website,
                          args=(url, interval, random_interval, min_interval, max_interval))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping all refreshes...")
            self.running = False
            for driver in self.drivers.values():
                try:
                    driver.quit()
                except:
                    pass
            sys.exit(0)

def main():
    load_dotenv()
    website = os.getenv("WEBSITE_URL")
    if not website:
        print("Error: WEBSITE_URL not found in .env")
        sys.exit(1)

    refresher = WebsiteRefresher()
    refresher.refresh_websites([website], interval=60)

if __name__ == "__main__":
    main()
