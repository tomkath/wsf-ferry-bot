#!/usr/bin/env python3
import os
import sys
from playwright.sync_api import sync_playwright
from simplepush import send

def test_playwright():
    """Test if Playwright is working"""
    print("Testing Playwright...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://www.wsdot.wa.gov')
            title = page.title()
            browser.close()
            print(f"✓ Playwright working - loaded page: {title}")
            return True
    except Exception as e:
        print(f"✗ Playwright error: {e}")
        return False

def test_simplepush(key):
    """Test SimplePush notification"""
    print("\nTesting SimplePush...")
    try:
        send(
            key=key,
            title="WSF Ferry Bot Test",
            message="This is a test notification from WSF Ferry Bot setup"
        )
        print("✓ SimplePush notification sent! Check your phone.")
        return True
    except Exception as e:
        print(f"✗ SimplePush error: {e}")
        return False

def test_ferry_page():
    """Test accessing the ferry reservation page"""
    print("\nTesting ferry reservation page...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://secureapps.wsdot.wa.gov/ferries/reservations/vehicle/SailingSchedule.aspx')
            
            # Check if we can find the form elements
            from_terminal = page.locator('#MainContent_dlFromTermList').is_visible()
            to_terminal = page.locator('#MainContent_dlToTermList').is_visible()
            
            browser.close()
            
            if from_terminal and to_terminal:
                print("✓ Ferry reservation page accessible")
                return True
            else:
                print("✗ Could not find ferry form elements")
                return False
    except Exception as e:
        print(f"✗ Ferry page error: {e}")
        return False

def main():
    print("WSF Ferry Bot Setup Test")
    print("========================\n")
    
    # Check for SimplePush key
    simplepush_key = os.environ.get('SIMPLEPUSH_KEY')
    if not simplepush_key:
        print("Please set SIMPLEPUSH_KEY environment variable or pass it as argument")
        print("Usage: python test_setup.py [SIMPLEPUSH_KEY]")
        if len(sys.argv) > 1:
            simplepush_key = sys.argv[1]
        else:
            sys.exit(1)
    
    # Run tests
    tests_passed = 0
    tests_total = 3
    
    if test_playwright():
        tests_passed += 1
    
    if test_ferry_page():
        tests_passed += 1
    
    if test_simplepush(simplepush_key):
        tests_passed += 1
    
    print(f"\n{tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("\n✓ All tests passed! Your setup is ready.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()