import os
import time
import random
import sys
from threading import Thread
from datetime import datetime
from typing import List, Dict
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv
from driver import driver_manager

load_dotenv()
website_url = os.getenv("WEBSITE_URL")

random_number = random.randint(5, 2000)
for _ in range(7):
    driver = driver_manager.create_driver()
    if driver:
        driver.get(website_url)
        driver.quit()
    else:
        print("Driver could not be created")