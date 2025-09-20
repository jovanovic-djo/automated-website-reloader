import os
import time
import random
from dotenv import load_dotenv
from driver import driver_manager

load_dotenv()
website_url = os.getenv("WEBSITE_URL")

timer = time.localtime()

random_number = random.randint(5, 2000)
driver = driver_manager.create_driver()
start_time = time.perf_counter()

if driver:
    try:
        driver.get(website_url)

        for _ in range(1, random_number):
            driver.refresh()
    finally:
        driver.quit()
else:
    print("Driver could not be created")
    
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")