#!/usr/bin/env python3
import json
import sys
import os

def acknowledge_notification(event_key: str):
    """Acknowledge a notification by its event key"""
    ack_file = '/tmp/ferry_bot_ack.json'
    
    # Load existing acknowledgments
    acks = {}
    if os.path.exists(ack_file):
        with open(ack_file, 'r') as f:
            acks = json.load(f)
    
    # Add acknowledgment
    acks[event_key] = True
    
    # Save back
    with open(ack_file, 'w') as f:
        json.dump(acks, f)
    
    print(f"Acknowledged notification: {event_key}")

def clear_acknowledgments():
    """Clear all acknowledgments"""
    ack_file = '/tmp/ferry_bot_ack.json'
    if os.path.exists(ack_file):
        os.remove(ack_file)
    print("Cleared all acknowledgments")

def list_acknowledgments():
    """List all current acknowledgments"""
    ack_file = '/tmp/ferry_bot_ack.json'
    if os.path.exists(ack_file):
        with open(ack_file, 'r') as f:
            acks = json.load(f)
            print("Current acknowledgments:")
            for key in acks:
                print(f"  - {key}")
    else:
        print("No acknowledgments found")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python acknowledge.py <event_key>")
        print("       python acknowledge.py --clear")
        print("       python acknowledge.py --list")
        sys.exit(1)
    
    if sys.argv[1] == '--clear':
        clear_acknowledgments()
    elif sys.argv[1] == '--list':
        list_acknowledgments()
    else:
        acknowledge_notification(sys.argv[1])