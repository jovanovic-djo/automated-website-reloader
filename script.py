import os
import time
import random
import sys
from threading import Thread
from datetime import datetime
from typing import List, Dict
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv

load_dotenv()
website_url = os.getenv("WEBSITE_URL")

print(website_url)