#!/usr/bin/env python3
import os
import sys

# Test SimplePush
try:
    from simplepush import send
    key = sys.argv[1] if len(sys.argv) > 1 else "wsfwsf"
    send(
        key=key,
        title="WSF Ferry Bot Test",
        message="Setup successful! Your bot is ready.",
        event="test_notification"
    )
    print("✓ SimplePush notification sent! Check your phone.")
except Exception as e:
    print(f"✗ SimplePush error: {e}")
    print("Make sure to run: pip install simplepush")