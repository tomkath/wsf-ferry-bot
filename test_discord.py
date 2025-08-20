#!/usr/bin/env python3
import requests
import datetime

def test_discord():
    webhook_url = "https://discord.com/api/webhooks/1407166559847186533/JPuOLv0ngomSU_p0ndnqlbVHlfEsH8qPQB_j6tpPcu3rTgHedOX_QRkpHp8kuC2qSeCk"
    
    print("Testing Discord webhook...")
    
    # Simple test message
    payload = {
        "content": "🤖 **WSF Ferry Bot Test**\\n\\nBot is now actively monitoring for ferries from **Orcas Island** to **Anacortes** on **September 20, 2025** (AM times only).\\n\\nYou'll receive notifications here when spots become available! 🚢"
    }
    
    try:
        print("Sending test message to Discord...")
        response = requests.post(webhook_url, json=payload, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 204:
            print("✅ SUCCESS: Discord webhook is working!")
            print("Check your Discord channel for the test message.")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            if response.text:
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == '__main__':
    test_discord()

