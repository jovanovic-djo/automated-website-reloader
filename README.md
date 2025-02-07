# Website Auto-Refresher

A Python script that automatically refreshes multiple websites simultaneously at specified intervals using Selenium and Chrome WebDriver.

## Features

- Open multiple websites in separate Chrome windows
- Refresh each website independently at fixed or random intervals
- Real-time refresh status and counts for each website
- Error handling and automatic recovery per window
- Clean browser shutdown on exit
- Threading support for parallel execution

## Prerequisites

Before running the script, make sure you have:

1. Python 3.6 or higher installed
2. Google Chrome browser installed
3. ChromeDriver that matches your Chrome version

## Installation

1. Clone this repository or download the script:
```bash
git clone <your-repository-url>
cd website-refresher
```

2. Install required Python package:
```bash
pip install selenium
```

3. Install ChromeDriver:
   - Visit https://sites.google.com/chromium.org/driver/
   - Download the version matching your Chrome browser
   - Extract the executable and add it to your system PATH

## Usage

### Basic Usage

Refresh a single website every 60 seconds:
```bash
python refresher.py https://example.com --interval 60
```

Refresh multiple websites simultaneously:
```bash
python refresher.py https://example1.com https://example2.com https://example3.com --interval 60
```

### Advanced Usage

Refresh multiple websites with random intervals between 30 and 90 seconds:
```bash
python refresher.py https://example1.com https://example2.com --random --min 30 --max 90
```

### Command Line Arguments

- `urls`: One or more website URLs to refresh (required)
- `-i, --interval`: Interval between refreshes in seconds (default: 60)
- `-r, --random`: Use random intervals between min and max values
- `--min`: Minimum interval for random timing (seconds)
- `--max`: Maximum interval for random timing (seconds)

## Stopping the Script

Press `Ctrl+C` to stop the script. All browser windows will close automatically.

## Error Handling

The script includes automatic recovery mechanisms for each window:
- Attempts to refresh the page if there's an error
- Reloads the entire page if refresh fails
- Restarts the browser if page reload fails
- Each window operates independently - if one fails, others continue running
- 

###### Used this a few times for harmless pranks on GitHub. Boosted views for a few developers with "view counters" on their profile's README.md files.
