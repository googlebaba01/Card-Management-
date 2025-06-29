#!/usr/bin/env python3
"""
Test script to verify setup and dependencies
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import asyncio
        print("✅ asyncio")
    except ImportError as e:
        print(f"❌ asyncio: {e}")
        return False
    
    try:
        from playwright.async_api import async_playwright
        print("✅ playwright")
    except ImportError as e:
        print(f"❌ playwright: {e}")
        return False
    
    try:
        import openai
        print("✅ openai")
    except ImportError as e:
        print(f"❌ openai: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    return True

def test_local_imports():
    """Test if local modules can be imported"""
    print("\n🔍 Testing local imports...")
    
    try:
        from src.browser_manager import AdvancedBrowserManager
        print("✅ browser_manager")
    except ImportError as e:
        print(f"❌ browser_manager: {e}")
        return False
    
    try:
        from src.captcha_handler import CaptchaHandler
        print("✅ captcha_handler")
    except ImportError as e:
        print(f"❌ captcha_handler: {e}")
        return False
    
    try:
        from src.platform_detector import PlatformDetector
        print("✅ platform_detector")
    except ImportError as e:
        print(f"❌ platform_detector: {e}")
        return False
    
    try:
        from config.settings import PLATFORMS, CREDENTIALS
        print("✅ settings")
    except ImportError as e:
        print(f"❌ settings: {e}")
        return False
    
    return True

def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\n🔍 Testing environment file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file exists")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required variables
    required_vars = ['AMAZON_EMAIL', 'AMAZON_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("📝 Please edit .env file with your credentials")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_playwright_browser():
    """Test if Playwright browser can be launched"""
    print("\n🔍 Testing Playwright browser...")
    
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def test_browser():
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto('https://www.google.com')
            await browser.close()
            await playwright.stop()
        
        asyncio.run(test_browser())
        print("✅ Playwright browser test successful")
        return True
        
    except Exception as e:
        print(f"❌ Playwright browser test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing E-commerce Automation Setup")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test local imports
    if not test_local_imports():
        all_tests_passed = False
    
    # Test environment file
    if not test_env_file():
        all_tests_passed = False
    
    # Test Playwright browser
    if not test_playwright_browser():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Setup is complete.")
        print("\n📋 You can now run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Try running: python setup.py")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 