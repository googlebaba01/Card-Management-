import os
from dotenv import load_dotenv

load_dotenv()

# Platform configurations
PLATFORMS = {
    'amazon': {
        'base_url': 'https://www.amazon.in',
        'login_url': 'https://www.amazon.in/ap/signin',
        'selectors': {
            'email_input': '#ap_email',
            'password_input': '#ap_password',
            'continue_button': '#continue',
            'signin_button': '#signInSubmit',
            'add_to_cart': '#add-to-cart-button',
            'cart_icon': '#nav-cart',
            'proceed_to_checkout': 'name="proceedToRetailCheckout"'
        }
    },
    'flipkart': {
        'base_url': 'https://www.flipkart.com',
        'login_url': 'https://www.flipkart.com/account/login',
        'selectors': {
            'email_input': 'input[type="text"]',
            'password_input': 'input[type="password"]',
            'login_button': 'button[type="submit"]',
            'add_to_cart': 'button._2KpZ6l._2U9uOA._3v1-ww',
            'cart_icon': 'a[href="/viewcart"]',
            'place_order': 'button span:has-text("PLACE ORDER")'
        }
    }
}

# User credentials
CREDENTIALS = {
    'amazon': {
        'email': os.getenv('AMAZON_EMAIL'),
        'password': os.getenv('AMAZON_PASSWORD'),
        'phone': os.getenv('AMAZON_PHONE')
    },
    'flipkart': {
        'email': os.getenv('FLIPKART_EMAIL'),
        'password': os.getenv('FLIPKART_PASSWORD')
    }
}

# User details for checkout
USER_DETAILS = {
    'name': os.getenv('USER_NAME'),
    'phone': os.getenv('USER_PHONE'),
    'address': os.getenv('USER_ADDRESS'),
    'city': os.getenv('USER_CITY'),
    'pincode': os.getenv('USER_PINCODE')
}

# Browser settings
BROWSER_CONFIG = {
    'headless': True,
    'viewport': {'width': 1920, 'height': 1080},
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Ultra-fast performance settings
ULTRA_FAST_CONFIG = {
    'browser_startup_timeout': 30000,  # 30 seconds
    'navigation_timeout': 8000,        # 8 seconds
    'element_timeout': 5000,           # 5 seconds
    'click_timeout': 3000,             # 3 seconds
    'typing_delay': 5,                 # 5ms between characters
    'click_delay': 0.1,                # 100ms before/after clicks
    'navigation_delay': 0.3,           # 300ms after navigation
    'login_wait': 1.5,                 # 1.5 seconds for login
    'cart_wait': 1.0,                  # 1 second for cart operations
    'captcha_timeout': 2,              # 2 seconds for captcha handling
    'parallel_operations': True,       # Enable parallel operations
    'minimal_verification': True,      # Skip detailed verification
    'fast_fallback': True              # Use fast fallbacks
}

# Performance optimization flags
PERFORMANCE_FLAGS = {
    'disable_images': True,            # Disable image loading
    'disable_css': False,              # Keep CSS for layout
    'disable_javascript': False,       # Keep JS for functionality
    'disable_animations': True,        # Disable CSS animations
    'disable_media': True,             # Disable media loading
    'disable_fonts': True,             # Disable custom fonts
    'disable_plugins': True,           # Disable browser plugins
    'disable_extensions': True,        # Disable browser extensions
    'disable_logging': True,           # Disable console logging
    'disable_background_networking': True,
    'disable_background_timer_throttling': True,
    'disable_backgrounding_occluded_windows': True,
    'disable_renderer_backgrounding': True
}