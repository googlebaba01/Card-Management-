﻿# 🛒 E-commerce Automation Tool

A fast and efficient automation tool for Amazon that adds products to cart and proceeds to checkout automatically. Optimized to complete the entire flow in under 25 seconds.

## ✨ Features

- **Lightning Fast**: Optimized to complete automation in under 25 seconds
- **AI-Powered Captcha Solving**: Uses OpenAI Vision API to solve text captchas automatically
- **Anti-Detection**: Advanced browser stealth techniques to avoid bot detection
- **Smart Error Handling**: Robust error recovery and fallback mechanisms
- **Multi-Platform Support**: Currently supports Amazon (easily extensible to other platforms)

## 🚀 Quick Start

### 1. Setup

```bash
# Clone or download the project
cd ecommerce-automation

# Run the setup script
python setup.py
```

### 2. Configure Credentials

Edit the `.env` file with your Amazon credentials:

```env
# Amazon Credentials
AMAZON_EMAIL=your_email@example.com
AMAZON_PASSWORD=your_password

# Optional: OpenAI API Key for AI captcha solving
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run Automation

```bash
python main.py
```

Enter the Amazon product URL when prompted, and the tool will automatically:
1. Log in to your Amazon account
2. Navigate to the product page
3. Add the product to cart
4. Proceed to checkout
5. Return the checkout URL

## 🔧 Manual Setup (Alternative)

If the setup script doesn't work, follow these steps manually:

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers

```bash
playwright install chromium
```

### Create Environment File

```bash
# Copy the example file
cp env_example.txt .env

# Edit .env with your credentials
```

## 🤖 AI Captcha Solving

The tool includes AI-powered captcha solving using OpenAI's Vision API:

1. **Automatic Detection**: Detects various types of captchas
2. **AI Vision**: Uses GPT-4 Vision to read and solve text captchas
3. **Manual Fallback**: If AI fails, pauses for manual solving

To enable AI captcha solving:
1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Add it to your `.env` file: `OPENAI_API_KEY=your_key_here`

## ⚡ Performance Optimizations

The tool is optimized for speed with several techniques:

- **Fast Mode**: Reduced delays and faster interactions
- **Parallel Processing**: Concurrent operations where possible
- **Smart Navigation**: Direct URLs and optimized page loading
- **Efficient Selectors**: Multiple fallback selectors for reliability
- **Timeout Optimization**: Reduced timeouts for faster failure detection

## 🛡️ Anti-Detection Features

- **Browser Stealth**: Removes automation indicators
- **Human-like Behavior**: Random delays and mouse movements
- **User Agent Rotation**: Multiple realistic user agents
- **Header Spoofing**: Realistic browser headers
- **Permission Mocking**: Simulates real browser permissions

## 📁 Project Structure

```
ecommerce-automation/
├── main.py                 # Main automation script
├── setup.py               # Setup and installation script
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
├── config/
│   └── settings.py       # Configuration and credentials
├── src/
│   ├── browser_manager.py    # Browser automation and stealth
│   ├── captcha_handler.py    # Captcha detection and solving
│   └── platform_detector.py  # Platform detection logic
└── logs/                 # Screenshots and debug logs
```

## 🔍 Troubleshooting

### Common Issues

1. **Login Timeout**
   - Check your internet connection
   - Verify credentials in `.env` file
   - Try running again (Amazon may have temporary issues)

2. **Element Not Found**
   - Amazon may have updated their website
   - Check the logs folder for screenshots
   - The tool has multiple fallback selectors

3. **Captcha Issues**
   - Enable AI solving with OpenAI API key
   - Solve manually when prompted
   - Some captchas require manual intervention

4. **Browser Issues**
   - Ensure Playwright browsers are installed
   - Try running `playwright install chromium`
   - Check system requirements

### Debug Mode

The browser runs in visible mode by default for debugging. To see what's happening:
- Watch the browser window during automation
- Check the console output for detailed logs
- Review screenshots in the `logs/` folder

## ⚠️ Important Notes

- **Use Responsibly**: Respect website terms of service
- **Rate Limiting**: Don't run too frequently to avoid being blocked
- **Credentials**: Keep your `.env` file secure and never commit it
- **Captchas**: Some captchas may require manual solving
- **Testing**: Test with inexpensive items first

## 🔄 Extending to Other Platforms

The tool is designed to be easily extensible. To add support for other platforms:

1. Add platform configuration in `config/settings.py`
2. Update `src/platform_detector.py`
3. Add platform-specific selectors and logic
4. Test thoroughly
