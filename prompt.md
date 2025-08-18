# WSF Ferry Bot - Development Prompt

This document contains the conversation that led to the creation of the WSF Ferry Bot, with sensitive information removed for reference.

## Initial Request

```
hey new project time! take this: https://github.com/wakawaka54/wsf-bot but instead of notifying via discord, I want you to: 

check for availability
if found, put in cart
notify, and notify every min until you acknowledge using simplepush
Test on available routes, if it works, change the routes to the ones you care. ship!

oh i want this ran in github actions, every minute.
```

## Key Requirements Identified

1. **Base Project**: Fork from https://github.com/wakawaka54/wsf-bot (Discord-based ferry checker)
2. **Notification Method**: Replace Discord with SimplePush notifications
3. **Cart Functionality**: Automatically add available ferries to cart
4. **Persistent Notifications**: Continue notifying every minute until acknowledged
5. **Deployment**: Run on GitHub Actions every minute
6. **Configuration**: Support for preferred ferry times

## SimplePush Credentials
- Key: `[REDACTED]`

## WSF Account Credentials  
- Username: `[REDACTED]`
- Password: `[REDACTED]`

## Development Process

### Phase 1: Analysis and Planning
- Analyzed original wsf-bot structure using Playwright for ferry schedule checking
- Identified need to replace Discord webhooks with SimplePush API
- Created todo list for systematic development

### Phase 2: Core Implementation
- Built ferry_bot.py with SimplePush integration
- Added WSF account login functionality
- Implemented preferred times feature
- Created acknowledgment system for stopping notifications

### Phase 3: GitHub Actions Integration
- Created workflows for every-minute execution
- Added environment variable support for secrets
- Implemented manual acknowledgment workflow

### Phase 4: Testing and Debugging
- Discovered date input formatting issues with WSF website
- Fixed JavaScript-based date field population
- Identified radio button selection vs "Add to Cart" buttons
- Encountered reCAPTCHA during cart addition process

### Phase 5: Simplification
After discovering CAPTCHA requirements, simplified to notification-only approach:
- Removed cart interaction complexity
- Focus on instant notifications when availability detected
- Include direct booking link in notifications
- Cleaner, more reliable approach

## Final Architecture

### Core Components
1. **ferry_bot.py** - Main monitoring script
2. **acknowledge.py** - Notification acknowledgment utility  
3. **GitHub Actions Workflows**:
   - `ferry-check.yml` - Runs every minute
   - `acknowledge.yml` - Manual acknowledgment workflow
4. **Configuration**:
   - Environment variables for GitHub Actions
   - YAML config for local testing

### Key Features
- Playwright-based web scraping of WSF reservation system
- SimplePush notifications with event keys for acknowledgment
- Preferred time prioritization
- Persistent state management in /tmp files
- Headless browser operation for GitHub Actions

### Configuration Example
```yaml
simplepush:
  key: "your_key_here"

wsf:
  username: "your_email@domain.com"
  password: "your_password"

requests:
  - terminal_from: "port townsend"
    terminal_to: "coupeville"
    sailing_date: "08/20/2025"
    vehicle_size: "under_22"
    vehicle_height: "up_to_7_2"
    preferred_times:
      - "9:40 AM"
      - "3:00 PM"
```

## GitHub Secrets Required
- `SIMPLEPUSH_KEY`: SimplePush notification key
- `WSF_USERNAME`: WSF account username  
- `WSF_PASSWORD`: WSF account password
- `FERRY_REQUESTS`: JSON array of route configurations

## Technical Challenges Solved

1. **Date Input**: WSF website requires JavaScript execution to properly set date values
2. **Schedule Parsing**: Extract ferry times and availability from dynamic table
3. **CAPTCHA Detection**: Identify when human intervention is required
4. **State Management**: Track notification history and acknowledgments
5. **Preferred Times**: Match user preferences against available ferry times

## Final Outcome

A notification-only ferry monitoring bot that:
- Monitors WSF availability every minute via GitHub Actions
- Sends instant SimplePush notifications when spots become available
- Prioritizes user-specified departure times
- Includes direct booking links for immediate reservation
- Continues alerting until acknowledged by user

The simplified approach avoids CAPTCHA complications while still providing significant advantage through automated monitoring and instant notifications.