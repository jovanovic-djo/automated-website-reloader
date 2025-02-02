import requests
import time
import random
from datetime import datetime
import argparse
from urllib.parse import urlparse
import sys

def validate_url(url):
    """Validate if the provided URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def refresh_website(url, interval, random_interval=False, min_interval=None, max_interval=None):
    """
    Continuously refresh a website at specified intervals.
    
    Args:
        url (str): The website URL to refresh
        interval (int): Base interval in seconds between refreshes
        random_interval (bool): Whether to use random intervals
        min_interval (int): Minimum interval for random timing
        max_interval (int): Maximum interval for random timing
    """
    
    if not validate_url(url):
        print(f"Error: Invalid URL format - {url}")
        sys.exit(1)
    
    # Initialize session to maintain cookies and connection
    session = requests.Session()
    
    # Add headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    refresh_count = 0
    
    try:
        while True:
            try:
                # Make the request
                response = session.get(url, headers=headers, timeout=10)
                refresh_count += 1
                
                # Print status
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Refresh #{refresh_count}: Status Code {response.status_code}")
                
                # Calculate wait time
                if random_interval and min_interval and max_interval:
                    wait_time = random.uniform(min_interval, max_interval)
                else:
                    wait_time = interval
                
                # Wait before next refresh
                time.sleep(wait_time)
                
            except requests.RequestException as e:
                print(f"Error during request: {e}")
                print("Waiting 30 seconds before retrying...")
                time.sleep(30)
                continue
            
    except KeyboardInterrupt:
        print("\nScript stopped by user")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Auto-refresh a website at specified intervals')
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

"""
Example of run command: python script.py https://youtube.com --random --min 30 --max 90
"""

