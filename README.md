# WSF Ferry Bot - Automated Ferry Availability Monitor

Monitor Washington State Ferry availability and receive instant notifications when spots open up. Runs automatically every 5 minutes using GitHub Actions (free). Supports multiple notification methods including mobile push notifications and Discord webhooks.

## What This Does

- 🔄 **Checks ferry availability** every 5 minutes for your specified routes
- 📱 **Sends instant notifications** when ferry spots become available
- ⏰ **Time filtering** - only notify for specific time ranges
- 🚗 **Vehicle options** - support for cars, SUVs, trucks, and RVs
- 🆓 **Completely free** - runs on GitHub Actions
- 🛠️ **No coding required** - just edit configuration files

## Step-by-Step Setup Guide

### Step 1: Set Up Notifications

Choose your preferred notification method:

#### Option A: Mobile Push Notifications (SimplePush)
Perfect for getting alerts directly on your phone.

1. **Install SimplePush app**:
   - [iPhone](https://apps.apple.com/app/simplepush/id1513932016) or [Android](https://play.google.com/store/apps/details?id=com.simplepush)
2. **Get your key** from the app (save for Step 4)

#### Option B: Discord Notifications
Perfect for teams, desktop notifications, or shared monitoring.

1. **Create Discord webhook**:
   - In your Discord server, go to **Server Settings** → **Integrations** → **Webhooks**
   - Click **"Create Webhook"** or **"New Webhook"**
   - Give it a name like "Ferry Bot" and choose the channel where alerts should appear
   - Click **"Copy Webhook URL"** (save this for Step 4)
   - **Example format**: `https://discord.com/api/webhooks/1234567890/abcdef123456...`

2. **Test your webhook** (optional but recommended):
   - You can test your webhook URL using our test script (see Testing section below)

### Step 2: Copy This Project to Your GitHub

1. **Create a GitHub account** if you don't have one:
   - Go to [github.com](https://github.com) and click "Sign up"
   - It's free

2. **Fork this repository**:
   - Click the "Fork" button at the top right of this page
   - This creates your own copy of the bot

### Step 3: Configure Which Ferries to Monitor

The `ferry_requests.json` file defines which ferry routes to monitor. This file is used by both GitHub Actions and local development.

1. In your forked repository, click on the file `ferry_requests.json`
2. Click the pencil icon (✏️) to edit  
3. Replace the contents with your desired routes:

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

**Configuration Guide:**

- **sailing_date**: Use format "MM/DD/YYYY" (e.g., "12/25/2024")
- **terminal_from** and **terminal_to** must be one of:
  - `anacortes`
  - `friday harbor`
  - `coupeville`
  - `lopez island`
  - `orcas island`
  - `port townsend`
  - `shaw island`
- **vehicle_size** options:
  - `normal` - Standard vehicles under 22 feet (recommended)
  - `under_22` - Legacy format (same as normal)
- **vehicle_height** options:
  - `normal` - Vehicles up to 7'2" tall (most cars)
  - `tall` - Vehicles 7'2" to 7'6" tall (SUVs, small trucks)
  - `tallxl` - Vehicles 7'6" to 13' tall (large trucks, RVs)
  - Legacy options still supported: `up_to_7_2`, `7_2_to_7_6`, `7_6_to_13`
- **Time filtering** (all optional):
  - `sailing_time_from`: Only ferries at or after this time (e.g., `"8:00 AM"`)
  - `sailing_time_to`: Only ferries at or before this time (e.g., `"6:00 PM"`)
  - Both: Creates a time range (e.g., 8 AM to 6 PM only)
  - Neither: Monitor ALL available times
  - Use 12-hour format with AM/PM

**Multiple Routes Example:**
```json
[
  {
    "terminal_from": "anacortes",
    "terminal_to": "friday harbor",
    "sailing_date": "12/25/2024",
    "vehicle_size": "normal",
    "vehicle_height": "normal",
    "sailing_time_from": "8:00 AM",
    "sailing_time_to": "4:00 PM"
  },
  {
    "terminal_from": "port townsend",
    "terminal_to": "coupeville",
    "sailing_date": "12/26/2024",
    "vehicle_size": "normal",
    "vehicle_height": "tall",
    "sailing_time_from": "2:00 PM"
  }
]
```

**How It Works:**
- **Time filtering**: Use `sailing_time_from` and/or `sailing_time_to` to filter by time
- **Legacy support**: Old `preferred_times` format still works
- **Flexible**: Can specify just start time, just end time, or both

4. Click "Commit changes" at the bottom

### Step 4: Configure GitHub Settings

#### For SimplePush Users:
1. In your repository, go to **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - **Name**: `SIMPLEPUSH_KEY`, **Secret**: Your SimplePush key (e.g., `Wsfwsf`)
   - Optional: `SIMPLEPUSH_PASSWORD` and `SIMPLEPUSH_SALT` for encrypted notifications

#### For Discord Users:
1. In your repository, go to **Settings** → **Secrets and variables** → **Actions**
2. **Variables tab**: Click **"New repository variable"** and add:
   - **Name**: `NOTIFICATION_TYPE`
   - **Value**: `discord`
3. **Secrets tab**: Click **"New repository secret"** and add:
   - **Name**: `DISCORD_WEBHOOK_URL`
   - **Secret**: Your Discord webhook URL (the full `https://discord.com/api/webhooks/...` URL)
4. **Test your setup** (recommended):
   - Go to **Actions** tab → **Check Ferry Availability** → **Run workflow**
   - The first run will send a test Discord message to verify your webhook works

### Step 5: Enable the Bot

1. Go to the **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. Click on "Check Ferry Availability" workflow
4. Click "Enable workflow"

That's it! The bot will now check every 5 minutes and send notifications when ferries are available.

## Testing Your Setup

### Discord Webhook Test (Local)
To test your Discord webhook locally before running on GitHub:

1. **Install Python dependencies** (if testing locally):
   ```bash
   pip install requests pyyaml
   ```

2. **Create a test script** and run it:
   ```bash
   # Create test_webhook.py with your webhook URL
   python test_webhook.py
   ```

3. **Check your Discord channel** for the test message.

### GitHub Actions Test
1. **Test the full workflow**:
   - Go to **Actions** tab in your repository
   - Click "Check Ferry Availability"  
   - Click "Run workflow" → "Run workflow"
   - Watch the logs to ensure it's working

2. **First run behavior**:
   - The first time you run with Discord notifications, it will send a test message
   - Subsequent runs will only notify when ferries are actually available

3. **You'll receive notifications when ferries are available with**:
   - 🚢 Ferry route and date
   - 🕐 All available times  
   - 🚗 Your vehicle configuration
   - 🔗 Direct booking link to WSF website

## What to Expect

When ferries become available, you'll receive instant notifications with:
- ✅ Ferry route and date
- 🕐 All available times
- 🚗 Your vehicle configuration
- 🔗 Direct booking link to WSF website

Notifications continue every 5 minutes until acknowledged, ensuring you don't miss available spots.

## Troubleshooting

**Not getting notifications?**
- Check your notification credentials are correct (keys are case-sensitive!)
- Verify notification permissions are enabled
- Look at the Actions tab in GitHub to see if the bot is running without errors

**Bot shows errors?**
- Double-check your `ferry_requests.json` formatting
- Make sure terminal names are lowercase
- Verify dates are in MM/DD/YYYY format

**Want to stop the bot?**
- Go to Actions → Check Ferry Availability → ⋯ → Disable workflow

## File Structure

Understanding the configuration files:

### **For GitHub Actions (Recommended)**
- **`ferry_requests.json`** - Define which ferries to monitor (edit directly in GitHub)
- **GitHub Secrets/Variables** - Store notification credentials securely
- **No local files needed** - everything configured through GitHub interface

### **For Local Development**  
- **`ferry_requests.json`** - Same ferry routes as GitHub Actions
- **`config.yaml`** - Local notification credentials (copy from `config.yaml.example`)
- **Both files required** - ferry routes + local notification settings

### **Example Files (Templates)**
- **`config.yaml.example`** - Template for creating local `config.yaml`
- **`ferry_requests.json.example`** - Template showing ferry request format

## Local Development

For developers who want to run locally:

1. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **Configure notifications locally:**
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your Discord webhook URL or SimplePush key
```

3. **Configure ferry routes:**
```bash
# Edit ferry_requests.json with your desired routes
# (same format used by GitHub Actions)
```

4. **Run:** `python ferry_bot.py`

**Note:** Local development uses `config.yaml` for credentials, while GitHub Actions uses environment variables for security.

## Important Notes

- The bot checks availability only - it does not make reservations
- The bot only monitors vehicle reservations (not walk-on passengers)

### GitHub Actions Usage

- **Public repositories get unlimited free Actions minutes**
- Each check takes about 1 minute to run
- Running every 5 minutes = checking 288 times per day
- No cost as long as the repository is public

### Changing Check Frequency

To check more or less frequently, edit `.github/workflows/check_ferries.yml` and change the cron schedule:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes (current)
```

**Common schedules:**
- Every minute: `'* * * * *'`
- Every 5 minutes: `'*/5 * * * *'` (default)
- Every 10 minutes: `'*/10 * * * *'`
- Every 30 minutes: `'*/30 * * * *'`
- Every hour: `'0 * * * *'`

**Note:** GitHub Actions may not guarantee runs more frequently than every 5 minutes during busy periods.

## Supported Features

### ✅ Vehicle Types
- **Cars** (normal height)
- **SUVs & Small Trucks** (tall)
- **Large Trucks & RVs** (tallxl)
- All vehicles under 22 feet in length

### ✅ All Ferry Routes
- Anacortes ↔ San Juan Islands
- Port Townsend ↔ Coupeville
- All Washington State Ferry vehicle routes

### ✅ Flexible Time Filtering
- Specific time ranges (8 AM - 6 PM)
- Open-ended (after 2 PM, before noon)
- No restrictions (all times)

### ✅ Notification Methods
- Mobile push notifications (SimplePush)
- Discord webhook notifications
- Extensible for additional methods

## Support

Having issues? [Create an issue](https://github.com/YOUR_USERNAME/wsf-ferry-bot/issues) in your forked repository.