import asyncio
import logging
from config.settings import PLATFORMS, CREDENTIALS

class LoginHandler:
    def __init__(self, platform):
        self.platform = platform
        self.config = PLATFORMS[platform]
        self.credentials = CREDENTIALS[platform]
    
    async def login(self, page):
        """Automated login for the platform"""
        try:
            print(f"Starting login for {self.platform}...")
            
            # Navigate to login page
            await page.goto(self.config['login_url'], wait_until='networkidle')
            await asyncio.sleep(2)
            
            if self.platform == 'amazon':
                return await self._amazon_login(page)
            elif self.platform == 'flipkart':
                return await self._flipkart_login(page)
                
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    async def _amazon_login(self, page):
        """Amazon-specific login flow"""
        try:
            # Enter email
            await page.fill(self.config['selectors']['email_input'], 
                          self.credentials['email'])
            await page.click(self.config['selectors']['continue_button'])
            await asyncio.sleep(2)
            
            # Enter password
            await page.fill(self.config['selectors']['password_input'], 
                          self.credentials['password'])
            await page.click(self.config['selectors']['signin_button'])
            await asyncio.sleep(3)
            
            # Check if login successful
            if await page.locator('#nav-link-accountList').count() > 0:
                print("Amazon login successful!")
                return True
            else:
                print("Amazon login failed!")
                return False
                
        except Exception as e:
            print(f"Amazon login error: {str(e)}")
            return False
    
    async def _flipkart_login(self, page):
        """Flipkart-specific login flow"""
        try:
            # Close any popups
            close_popup = page.locator('button._2KpZ6l._2doB4z')
            if await close_popup.count() > 0:
                await close_popup.click()
            
            # Enter email/phone
            await page.fill('input[type="text"]', self.credentials['email'])
            await page.fill('input[type="password"]', self.credentials['password'])
            await page.click('button[type="submit"]')
            await asyncio.sleep(3)
            
            # Check if login successful
            if await page.locator('[data-testid="account-menu"]').count() > 0:
                print("Flipkart login successful!")
                return True
            else:
                print("Flipkart login failed!")
                return False
                
        except Exception as e:
            print(f"Flipkart login error: {str(e)}")
            return False