# WSF Ferry Bot - Automated Ferry Availability Monitor

Monitor Washington State Ferry availability and receive instant notifications when spots open up. Runs automatically every 5 minutes using GitHub Actions (completely free). Get alerts on Discord or your phone when ferries become available!

## What This Does

- 🔄 **Checks ferry availability** every 5 minutes for your routes
- 📱 **Sends instant notifications** when ferry spots open up
- ⏰ **Time filtering** - only notify for specific time ranges
- 🚗 **All vehicle types** - cars, SUVs, trucks, and RVs
- 🆓 **Completely free** - runs on GitHub Actions
- 🛠️ **No coding required** - just edit configuration files

## 5-Minute Setup Guide

### Step 1: Choose Your Notification Method

Pick **one** option:

#### Option A: Phone Notifications (SimplePush)
1. Install SimplePush app: [iPhone](https://apps.apple.com/app/simplepush/id1513932016) or [Android](https://play.google.com/store/apps/details?id=com.simplepush)
2. Open the app and copy your key (save for Step 4)

#### Option B: Discord Notifications (Recommended)
1. In your Discord server: **Server Settings** → **Integrations** → **Webhooks**
2. Click **"Create Webhook"** 
3. Name it "Ferry Bot" and choose your channel
4. Click **"Copy Webhook URL"** (save for Step 4)

### Step 2: Copy This Bot to Your GitHub

1. **Create a free GitHub account** at [github.com](https://github.com) (if you don't have one)
2. **Click the "Fork" button** at the top right of this page
3. This creates your own copy of the ferry bot

### Step 3: Configure Your Ferry Routes

1. **In your forked repository**, click `ferry_requests.json`
2. **Click the pencil icon** (✏️) to edit
3. **Replace everything** with your ferry routes:

```json
[
  {
    "terminal_from": "anacortes",
    "terminal_to": "friday harbor", 
    "sailing_date": "12/25/2024",
    "vehicle_size": "normal",
    "vehicle_height": "normal",
    "sailing_time_from": "8:00 AM",
    "sailing_time_to": "6:00 PM"
  }
]
```

**Ferry Terminals** (use exactly as shown):
- `anacortes`, `friday harbor`, `lopez island`, `orcas island`, `shaw island`
- `port townsend`, `coupeville`

**Vehicle Options:**
- **Size**: `normal` (under 22 feet - covers most vehicles)
- **Height**: `normal` (up to 7'2"), `tall` (7'2"-7'6"), `tallxl` (7'6"-13')

**Time Filtering** (optional):
- `sailing_time_from`: "8:00 AM" (earliest time you want)
- `sailing_time_to`: "6:00 PM" (latest time you want)
- Leave both out to monitor ALL ferry times

4. **Click "Commit changes"** at the bottom

### Step 4: Set Up Your Notifications

#### For Phone Notifications (SimplePush):
1. Go to **Settings** → **Secrets and variables** → **Actions** in your repository
2. **Secrets tab** → **"New repository secret"**:
   - Name: `SIMPLEPUSH_KEY`
   - Secret: (paste your SimplePush key)

#### For Discord Notifications:
1. Go to **Settings** → **Secrets and variables** → **Actions** in your repository
2. **Variables tab** → **"New repository variable"**:
   - Name: `NOTIFICATION_TYPE` 
   - Value: `discord`
3. **Secrets tab** → **"New repository secret"**:
   - Name: `DISCORD_WEBHOOK_URL`
   - Secret: (paste your Discord webhook URL)

### Step 5: Start the Bot

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Click **"Check Ferry Availability"** workflow
4. Click **"Enable workflow"**
5. **Test it**: Click **"Run workflow"** → **"Run workflow"**

**That's it!** Your bot will now check every 5 minutes and notify you when ferries are available.

## What to Expect

### First Run (Discord Only)
- Discord users get a one-time test message to confirm setup is working
- You won't see this test again unless you change your webhook URL

### Ferry Availability Alerts
When spots open up, you'll get notifications with:
- 🚢 **Ferry route and date**
- ⏰ **All available times** 
- 🔗 **Direct booking link** to reserve your spot

Example Discord notification:
```
🚢 Ferry Available! anacortes → friday harbor
Date: 12/25/2024
⭐ Preferred times: 8:30 AM, 2:30 PM
🚢 All times: 6:00 AM, 8:30 AM, 12:00 PM, 2:30 PM, 5:45 PM
🔗 Book now: https://secureapps.wsdot.wa.gov/ferries/reservations/...
```

## Advanced Configuration

### Multiple Routes
Add more ferry routes to monitor:

```json
[
  {
    "terminal_from": "anacortes",
    "terminal_to": "friday harbor",
    "sailing_date": "12/25/2024",
    "vehicle_size": "normal", 
    "vehicle_height": "normal"
  },
  {
    "terminal_from": "port townsend",
    "terminal_to": "coupeville", 
    "sailing_date": "12/26/2024",
    "vehicle_size": "normal",
    "vehicle_height": "tall"
  }
]
```

### Change Check Frequency
Edit `.github/workflows/check_ferries.yml` and change:
```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes (default)
```

**Common schedules:**
- Every 1 minute: `'* * * * *'`
- Every 10 minutes: `'*/10 * * * *'` 
- Every 30 minutes: `'*/30 * * * *'`
- Every hour: `'0 * * * *'`

## Troubleshooting

**Not getting notifications?**
- Check your notification credentials are correct (Discord webhook URL, SimplePush key)
- Verify you enabled the workflow in the Actions tab
- Look at the Actions tab for error messages

**Bot shows errors in Actions?**
- Check your `ferry_requests.json` formatting (use a JSON validator)
- Make sure terminal names are lowercase and exact
- Verify dates are in MM/DD/YYYY format

**Want to stop the bot?**
- Actions → Check Ferry Availability → ⋯ → Disable workflow

## Important Notes

- ✅ **Free forever** - GitHub Actions provides unlimited free minutes for public repositories
- ⚠️ **This bot only monitors availability** - it does not make reservations for you
- 🚗 **Vehicle reservations only** - does not monitor walk-on passenger availability
- ⏰ **5-minute intervals** - GitHub may delay runs during busy periods

## Support

Having issues? [Create an issue](https://github.com/keithah/wsf-ferry-bot/issues) in the main repository for help and bug reports.

---

## Local Development & Testing

**Note: This section is for developers who want to run the bot locally. Most users should use the GitHub Actions setup above.**

### Setup
1. **Clone your forked repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
3. **Create local config:**
   ```bash
   cp config.yaml.example config.yaml
   # Edit config.yaml with your Discord webhook URL or SimplePush key
   ```
4. **Edit ferry routes** in `ferry_requests.json`
5. **Run:** `python ferry_bot.py`

### File Structure
- **`ferry_requests.json`** - Ferry routes to monitor (shared with GitHub Actions)
- **`config.yaml`** - Local notification credentials (local development only)
- **GitHub Secrets** - Notification credentials for GitHub Actions (production)

### Local Testing
Create a simple webhook test:
```python
import requests

webhook_url = "your_discord_webhook_url_here"
payload = {"content": "Test message from ferry bot!"}
response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
```

**Security Note:** Local development uses `config.yaml` for credentials, while GitHub Actions uses encrypted environment variables for better security.