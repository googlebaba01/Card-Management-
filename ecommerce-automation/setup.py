#!/usr/bin/env python3
"""
Setup script for E-commerce Automation
"""
import os
import subprocess
import sys

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def install_playwright_browsers():
    """Install Playwright browsers"""
    print("🌐 Installing Playwright browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright browsers installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        return False
    return True

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('env_example.txt'):
        try:
            with open('env_example.txt', 'r') as f:
                content = f.read()
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("📝 Please edit .env file with your credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def create_logs_directory():
    """Create logs directory"""
    try:
        os.makedirs('logs', exist_ok=True)
        print("✅ Logs directory created")
        return True
    except Exception as e:
        print(f"❌ Failed to create logs directory: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up E-commerce Automation...")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Create logs directory
    if not create_logs_directory():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Amazon credentials")
    print("2. Run: python main.py")
    print("\n⚠️  Important:")
    print("- Keep your credentials secure")
    print("- The browser will be visible for debugging")
    print("- You may need to solve captchas manually")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 