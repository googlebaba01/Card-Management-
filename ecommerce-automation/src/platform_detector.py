from urllib.parse import urlparse
import re

class PlatformDetector:
    @staticmethod
    def detect_platform(product_url):
        """Detect e-commerce platform from URL"""
        domain = urlparse(product_url).netloc.lower()
        
        if 'amazon' in domain:
            return 'amazon'
        elif 'flipkart' in domain:
            return 'flipkart'
        elif 'myntra' in domain:
            return 'myntra'
        else:
            raise ValueError(f"Unsupported platform: {domain}")
    
    @staticmethod
    def extract_product_id(product_url, platform):
        """Extract product ID from URL"""
        if platform == 'amazon':
            match = re.search(r'/dp/([A-Z0-9]{10})', product_url)
            return match.group(1) if match else None
        
        elif platform == 'flipkart':
            match = re.search(r'/p/([^?]+)', product_url)
            return match.group(1) if match else None
        
        return None