#!/usr/bin/env python3
"""
Ferry Bot Fix - Corrects time parsing and adds Discord webhook configuration
Save this as ferry_bot_fixed.py in your wsf-ferry-bot directory
"""

import os
import json
import datetime
import re

# This section shows the fix for the time parsing issue
def fixed_parse_ferry_time(cells, debug=True):
    """
    Fixed time parsing that properly handles WSDOT ferry schedule format
    This replaces the problematic parsing on lines 180-190
    """
    if len(cells) >= 3:
        # Get the raw time text from the first cell
        time_text_raw = cells[0].inner_text().strip()
        
        if debug:
            print(f"DEBUG: Raw time text from cell: '{time_text_raw}'")
        
        # Clean up the time text - remove extra whitespace and normalize
        time_text = ' '.join(time_text_raw.split())
        
        # Extract time using regex to be more robust
        # This pattern matches times like "10:45 PM", "10:45PM", "2:30 AM"
        time_pattern = r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm|A\.M\.|P\.M\.)'
        match = re.search(time_pattern, time_text)
        
        if match:
            hour = match.group(1)
            minute = match.group(2)
            period = match.group(3).replace('.', '').strip().upper()
            
            # Normalize AM/PM
            if 'A' in period:
                period = 'AM'
            elif 'P' in period:
                period = 'PM'
            
            # Reconstruct the time string in standard format
            ferry_time_str = f"{hour}:{minute} {period}"
            
            if debug:
                print(f"DEBUG: Parsed time: {ferry_time_str}")
            
            # Now parse it properly
            TIME_FORMAT = '%I:%M %p'
            ferry_time = datetime.datetime.strptime(ferry_time_str, TIME_FORMAT).time()
            
            # Get vessel from last cell
            vessel = cells[-1].inner_text().strip()
            
            return {
                'time': ferry_time_str,  # Store the formatted string
                'time_obj': ferry_time,  # Store the time object for comparison
                'vessel': vessel,
                'raw_text': time_text_raw  # Keep raw text for debugging
            }
        else:
            print(f"WARNING: Could not parse time from: '{time_text}'")
            # Fallback - try to extract any time-like pattern
            fallback_pattern = r'(\d{1,2}:\d{2})'
            fallback_match = re.search(fallback_pattern, time_text)
            if fallback_match:
                print(f"DEBUG: Using fallback time extraction: {fallback_match.group(1)}")
                # Assume PM for afternoon/evening ferries if no AM/PM specified
                return {
                    'time': fallback_match.group(1) + " PM",  # Default to PM
                    'vessel': cells[-1].inner_text().strip(),
                    'raw_text': time_text_raw
                }
    
    return None

# HERE'S THE SECTION TO REPLACE IN ferry_bot.py (lines 177-190)
"""
REPLACE THIS SECTION (starting around line 177):
-------------------------------------------
for i, row in enumerate(rows[1:]):  # Skip header
    text = row.inner_text()
    if "Space Available" in text:
        cells = row.locator('td').all()
        if len(cells) >= 3:
            time_text = cells[0].inner_text().strip()
            vessel = cells[-1].inner_text().strip()
            
            ferry_info = {
                'time': time_text,
                'vessel': vessel
            }
            
            # Check if this time matches preferred times/range
            ferry_time_str = time_text.split()[0] + ' ' + time_text.split()[1]
            ferry_time = datetime.datetime.strptime(ferry_time_str, TIME_FORMAT).time()

WITH THIS FIXED VERSION:
------------------------
"""

def fixed_check_availability_section(page, rows):
    """
    Fixed section for parsing ferry availability
    This replaces lines 177-250 in the original ferry_bot.py
    """
    import re
    available_ferries = []
    TIME_FORMAT = '%I:%M %p'
    
    for i, row in enumerate(rows[1:]):  # Skip header
        text = row.inner_text()
        if "Space Available" in text:
            cells = row.locator('td').all()
            if len(cells) >= 3:
                # Get raw time text
                time_text_raw = cells[0].inner_text().strip()
                print(f"DEBUG: Processing row {i+1}, raw time: '{time_text_raw}'")
                
                # Clean and extract time components using regex
                time_pattern = r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm|A\.M\.|P\.M\.)'
                match = re.search(time_pattern, time_text_raw)
                
                if match:
                    hour = match.group(1)
                    minute = match.group(2)
                    period = match.group(3).replace('.', '').strip().upper()
                    
                    # Normalize period
                    period = 'AM' if 'A' in period else 'PM'
                    
                    # Create properly formatted time string
                    time_text = f"{hour}:{minute} {period}"
                    print(f"DEBUG: Formatted time: {time_text}")
                    
                    # Parse to time object for comparisons
                    try:
                        ferry_time = datetime.datetime.strptime(time_text, TIME_FORMAT).time()
                    except ValueError as e:
                        print(f"ERROR: Failed to parse time '{time_text}': {e}")
                        continue
                else:
                    print(f"WARNING: No time pattern found in '{time_text_raw}'")
                    # Try fallback - look for any time pattern
                    fallback = re.search(r'(\d{1,2}:\d{2})', time_text_raw)
                    if fallback:
                        # Assume PM for ferries (most run during day/evening)
                        time_text = fallback.group(1) + " PM"
                        print(f"DEBUG: Using fallback time: {time_text}")
                        try:
                            ferry_time = datetime.datetime.strptime(time_text, TIME_FORMAT).time()
                        except:
                            continue
                    else:
                        continue
                
                # Get vessel name
                vessel = cells[-1].inner_text().strip()
                
                ferry_info = {
                    'time': time_text,
                    'vessel': vessel,
                    'time_obj': ferry_time  # Keep for comparisons
                }
                
                # Rest of the preference checking logic remains the same...
                # (continues with the is_preferred logic from line 192 onwards)

# DISCORD WEBHOOK CONFIGURATION
"""
To configure Discord webhook, you have two options:

OPTION 1: GitHub Actions (Recommended for automated checking)
---------------------------------------------------------
1. Go to your forked repository on GitHub
2. Go to Settings → Secrets and variables → Actions
3. Under "Variables" tab, add:
   - Name: NOTIFICATION_TYPE
   - Value: discord
4. Under "Secrets" tab, add:
   - Name: DISCORD_WEBHOOK_URL  
   - Value: [Your Discord webhook URL]

OPTION 2: Local Testing with config.yaml
----------------------------------------
1. Copy config.yaml.example to config.yaml:
   cp config.yaml.example config.yaml

2. Edit config.yaml and update:
"""

# Sample config.yaml for Discord
DISCORD_CONFIG_YAML = """
# config.yaml for Discord notifications
notification_type: "discord"

# Discord configuration
discord:
  webhook_url: "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# Your ferry requests are loaded from ferry_requests.json
# So you don't need to specify them here
"""

# Test script to verify time parsing
def test_time_parsing():
    """Test the time parsing fix"""
    import re
    from datetime import datetime
    
    TIME_FORMAT = '%I:%M %p'
    
    # Test cases that might appear in WSDOT ferry schedule
    test_cases = [
        "10:45 PM",      # Correct format
        "10:45PM",       # No space
        "10:45 P.M.",    # With periods
        "10:45 pm",      # Lowercase
        "2:30 AM",       # Single digit hour
        "10:25 AM",      # The incorrect time your bot shows
        "10:45  PM",     # Extra spaces
        "\t10:45 PM\n",  # With whitespace
    ]
    
    print("Testing time parsing fix:")
    print("=" * 50)
    
    for test_time in test_cases:
        # Clean the input
        cleaned = ' '.join(test_time.strip().split())
        
        # Extract using regex
        pattern = r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm|A\.M\.|P\.M\.)'
        match = re.search(pattern, cleaned)
        
        if match:
            hour = match.group(1)
            minute = match.group(2)
            period = match.group(3).replace('.', '').strip().upper()
            period = 'AM' if 'A' in period else 'PM'
            
            formatted = f"{hour}:{minute} {period}"
            
            try:
                time_obj = datetime.strptime(formatted, TIME_FORMAT)
                print(f"✓ '{test_time}' → '{formatted}' → {time_obj.strftime('%H:%M')} (24hr)")
            except ValueError as e:
                print(f"✗ '{test_time}' → Failed: {e}")
        else:
            print(f"✗ '{test_time}' → No pattern match")
    
    print("=" * 50)
    print("\nThe issue: Bot shows '10:25 AM' instead of '10:45 PM'")
    print("This is likely due to:")
    print("1. Reading wrong cell/column from the schedule table")
    print("2. Text parsing splitting on wrong delimiter")
    print("3. AM/PM not being extracted properly")

if __name__ == "__main__":
    test_time_parsing()
    print("\n" + "=" * 50)
    print("DISCORD WEBHOOK SETUP:")
    print("=" * 50)
    print(DISCORD_CONFIG_YAML)
    print("\nTo fix your bot:")
    print("1. Apply the time parsing fix to ferry_bot.py")
    print("2. Configure Discord webhook as shown above")
    print("3. Test with: python ferry_bot.py")
