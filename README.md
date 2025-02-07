Website Auto-Refresher
A Python script that automatically refreshes a website at specified intervals using Selenium and Chrome WebDriver.
Features

Open website in Chrome browser
Refresh at fixed or random intervals
Real-time refresh status and counts
Error handling and automatic recovery
Clean browser shutdown on exit

Prerequisites
Before running the script, make sure you have:

Python 3.6 or higher installed
Google Chrome browser installed
ChromeDriver that matches your Chrome version

Installation

Clone this repository or download the script:

bashCopygit clone <your-repository-url>
cd website-refresher

Install required Python package:

bashCopypip install selenium

Install ChromeDriver:

Visit https://sites.google.com/chromium.org/driver/
Download the version matching your Chrome browser
Extract the executable and add it to your system PATH



Usage
Basic Usage
Refresh a website every 60 seconds:
bashCopypython refresher.py https://example.com --interval 60
Advanced Usage
Refresh with random intervals between 30 and 90 seconds:
bashCopypython refresher.py https://example.com --random --min 30 --max 90
Command Line Arguments

url: The website URL to refresh (required)
-i, --interval: Interval between refreshes in seconds (default: 60)
-r, --random: Use random intervals between min and max values
--min: Minimum interval for random timing (seconds)
--max: Maximum interval for random timing (seconds)

Stopping the Script
Press Ctrl+C to stop the script. The browser will close automatically.