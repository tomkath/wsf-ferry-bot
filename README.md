# WSF Ferry Bot - Get Instant Ferry Availability Notifications

This bot monitors Washington State Ferry availability and sends instant push notifications to your phone when spots become available. It checks every 5 minutes automatically using GitHub Actions (free).

## What This Does

- Checks ferry availability every 5 minutes for your specified routes
- Sends instant push notifications to your phone when spots open up
- Runs completely free on GitHub Actions
- No coding knowledge required to set up

## Step-by-Step Setup Guide

### Step 1: Choose Your Notification Method

Choose either **SimplePush** (mobile app) or **Discord** (webhook):

#### Option A: SimplePush (Mobile App)
1. **Install SimplePush** on your phone:
   - [iPhone App Store](https://apps.apple.com/app/simplepush/id1513932016)
   - [Android Google Play](https://play.google.com/store/apps/details?id=com.simplepush)

2. **Open SimplePush** and tap "Generate Key" to get your unique key
   - It will look something like: `HuxgBB` or `Wsfwsf`
   - **Write this down** - you'll need it in Step 4

#### Option B: Discord Webhook
1. **In your Discord server**, go to Server Settings → Integrations → Webhooks
2. **Click "New Webhook"** and choose a channel for notifications
3. **Copy the webhook URL** - it looks like:
   `https://discord.com/api/webhooks/123456789/abcdef...`
   - **Write this down** - you'll need it in Step 4

### Step 2: Copy This Project to Your GitHub

1. **Create a GitHub account** if you don't have one:
   - Go to [github.com](https://github.com) and click "Sign up"
   - It's free

2. **Fork this repository**:
   - Click the "Fork" button at the top right of this page
   - This creates your own copy of the bot

### Step 3: Configure Which Ferries to Monitor

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

#### For Discord Users:
1. In your repository, go to **Settings** → **Secrets and variables** → **Actions**
2. **Variables tab**: Add variable:
   - **Name**: `NOTIFICATION_TYPE`, **Value**: `discord`
3. **Secrets tab**: Add secret:
   - **Name**: `DISCORD_WEBHOOK_URL`, **Secret**: Your Discord webhook URL

#### For Both:
- Optional encrypted SimplePush: Add `SIMPLEPUSH_PASSWORD` and `SIMPLEPUSH_SALT` secrets if needed

### Step 5: Enable the Bot

1. Go to the **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. Click on "Check Ferry Availability" workflow
4. Click "Enable workflow"

That's it! The bot will now check every 5 minutes and send notifications to your SimplePush app when ferries are available.

## Testing Your Setup

1. To test immediately:
   - Go to **Actions** tab
   - Click "Check Ferry Availability"
   - Click "Run workflow" → "Run workflow"
   - Watch the logs to ensure it's working

2. You'll get a notification:

   **SimplePush (on your phone):**
   ```
   Ferry Available! anacortes → friday harbor
   Date: 12/25/2024
   🚢 All times: 8:30 AM, 10:45 AM, 2:30 PM, 4:15 PM
   🔗 Book now: https://secureapps.wsdot.wa.gov/...
   ```

   **Discord (in your channel):**
   Rich embed with ferry details, times, and booking link

## Stopping Notifications

The bot will keep notifying you every 5 minutes until you acknowledge. To stop notifications for a specific ferry, you'll need to note the event key from the SimplePush notification.

## Troubleshooting

**Not getting notifications?**
- Make sure SimplePush notifications are enabled in your phone settings
- Check that your SimplePush key is correct (case-sensitive!)
- Look at the Actions tab in GitHub to see if the bot is running

**Bot shows errors?**
- Double-check your `ferry_requests.json` formatting
- Make sure terminal names are lowercase
- Verify dates are in MM/DD/YYYY format

**Want to stop the bot?**
- Go to Actions → Check Ferry Availability → ⋯ → Disable workflow

## Local Development

For developers who want to run locally:

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

2. Copy `config.yaml.example` to `config.yaml` and add your SimplePush key

3. Run: `python ferry_bot.py`

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

## Vehicle Size Note

Currently only supports vehicles under 22 feet. To add support for larger vehicles, submit an issue or PR.

## Support

Having issues? [Create an issue](https://github.com/YOUR_USERNAME/wsf-ferry-bot/issues) in your forked repository.