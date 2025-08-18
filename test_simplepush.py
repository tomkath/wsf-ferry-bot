#!/usr/bin/env python3
import os
import yaml
from simplepush import send

def test_simplepush():
    # Try loading from config.yaml first
    if os.path.exists('config.yaml'):
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            key = config['simplepush']['key']
            password = config['simplepush'].get('password')
            salt = config['simplepush'].get('salt')
    else:
        # Fall back to environment variables
        key = os.environ.get('SIMPLEPUSH_KEY')
        password = os.environ.get('SIMPLEPUSH_PASSWORD')
        salt = os.environ.get('SIMPLEPUSH_SALT')
    
    if not key:
        print("ERROR: No SimplePush key found!")
        print("Please set it in config.yaml or SIMPLEPUSH_KEY environment variable")
        return
    
    print(f"Testing SimplePush with key: {key}")
    print(f"Key length: {len(key)}")
    print(f"First 3 chars: {key[:3]}...")
    
    try:
        # Send a test notification
        send(
            key=key,
            title="WSF Ferry Bot Test",
            message="If you see this, SimplePush is working correctly!",
            event="test_notification"
        )
        print("✅ Test notification sent successfully!")
        print("Check your SimplePush app for the notification.")
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")
        print("\nCommon issues:")
        print("1. Key is case-sensitive (you mentioned 'Wsfwsf')")
        print("2. Key might have extra spaces")
        print("3. Key might be incorrect")
        print("\nDouble-check your SimplePush key in the app.")

if __name__ == '__main__':
    test_simplepush()