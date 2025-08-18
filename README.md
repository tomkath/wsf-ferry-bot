# WSF Ferry Bot with SimplePush Notifications

This bot monitors Washington State Ferry availability and sends instant notifications via SimplePush when spots become available. It runs on GitHub Actions every minute.

## Features

- Checks ferry availability for specified routes every minute
- Prioritizes your preferred departure times
- Sends instant SimplePush notifications when spots open up
- Continues notifying every minute until acknowledged
- Includes direct booking link in notifications
- Runs automatically on GitHub Actions

## Setup

### 1. Fork this repository

### 2. Get SimplePush Key
1. Install SimplePush app on your phone
2. Get your key from the app

### 3. Configure GitHub Secrets
Go to Settings > Secrets and variables > Actions in your repository and add:

- `SIMPLEPUSH_KEY`: Your SimplePush key
- `SIMPLEPUSH_PASSWORD`: (Optional) For encrypted notifications
- `SIMPLEPUSH_SALT`: (Optional) For encrypted notifications
- `WSF_USERNAME`: Your WSF account username
- `WSF_PASSWORD`: Your WSF account password
- `FERRY_REQUESTS`: JSON array of ferry requests

Example `FERRY_REQUESTS`:
```json
[
  {
    "terminal_from": "anacortes",
    "terminal_to": "friday harbor",
    "sailing_date": "12/25/2024",
    "vehicle_size": "under_22",
    "vehicle_height": "up_to_7_2",
    "preferred_times": ["8:30 AM", "10:45 AM", "2:30 PM"]
  }
]
```

The `preferred_times` field is optional. If specified, the bot will:
- Try to add preferred times to cart first
- Still notify you of all available times
- Fall back to any available time if preferred times aren't available

### 4. Enable GitHub Actions
The workflow will run automatically every minute once enabled.

## Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Copy and configure `config.yaml.example` to `config.yaml`

3. Run the bot:
```bash
python ferry_bot.py
```

## Acknowledging Notifications

To stop notifications for a specific ferry:

```bash
python acknowledge.py <event_key>
```

The event key is sent with each SimplePush notification.

To clear all acknowledgments:
```bash
python acknowledge.py --clear
```

## Supported Terminals

- anacortes
- friday harbor
- coupeville
- lopez island
- orcas island
- port townsend
- shaw island

## Vehicle Sizes
- `under_22`: Vehicles under 22 feet

## Vehicle Heights
- `up_to_7_2`: Up to 7'2" tall
- `7_2_to_7_6`: 7'2" to 7'6" tall
- `7_6_to_13`: 7'6" to 13' tall