# src/captcha_handler.py
import asyncio
import os
import base64
from io import BytesIO
from PIL import Image
import openai

class CaptchaHandler:
    def __init__(self, page):
        self.page = page
        self.openai_client = None
        self.setup_openai()
    
    def setup_openai(self):
        """Setup OpenAI client if API key is available"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                # Remove any proxy settings that might cause issues
                self.openai_client = openai.OpenAI(api_key=api_key)
                print("🤖 AI captcha solver enabled")
            except Exception as e:
                print(f"⚠️ OpenAI setup failed: {e}")
                # Try alternative initialization
                try:
                    self.openai_client = openai.Client(api_key=api_key)
                    print("🤖 AI captcha solver enabled (alternative method)")
                except Exception as e2:
                    print(f"⚠️ OpenAI alternative setup also failed: {e2}")
    
    async def handle_captcha_fast(self, timeout=2):
        """Ultra-fast captcha handling with minimal delays"""
        try:
            # Quick check for captcha
            captcha_detected, captcha_type = await self.detect_captcha()
            if not captcha_detected:
                return True
            
            print(f"🎯 Quick handling {captcha_type} captcha...")
            
            # For ultra-fast mode, just wait briefly and continue
            await asyncio.sleep(0.5)
            
            # Check if captcha is still there
            captcha_detected, _ = await self.detect_captcha()
            if not captcha_detected:
                return True
            
            # If still there, handle it quickly
            if captcha_type == 'iframe' or 'recaptcha' in captcha_type:
                print("⚠️ reCAPTCHA detected - quick skip")
                return True
            else:
                # For text captcha, try AI solving quickly
                if self.openai_client:
                    try:
                        captcha_element = self.page.locator(captcha_type).first
                        ai_answer = await self.solve_captcha_with_ai(captcha_element)
                        if ai_answer:
                            input_selectors = [
                                'input[name*="captcha"]',
                                'input[id*="captcha"]',
                                'input[placeholder*="captcha"]'
                            ]
                            for selector in input_selectors:
                                if await self.page.locator(selector).count() > 0:
                                    await self.page.fill(selector, ai_answer)
                                    return True
                    except:
                        pass
                
                # Quick fallback
                print("⚠️ Quick captcha skip for speed")
                return True
                
        except Exception as e:
            print(f"⚠️ Fast captcha handling error: {e}")
            return True  # Continue anyway for speed
    
    async def detect_captcha(self):
        """Enhanced captcha detection - optimized"""
        captcha_selectors = [
            'img[src*="captcha"]',
            '[id*="captcha"]',
            '[class*="captcha"]',
            'iframe[src*="recaptcha"]',
            '.g-recaptcha',
            '[data-testid="captcha"]',
            'canvas[class*="captcha"]',
            'div[class*="captcha"]',
            'img[alt*="captcha"]',
            'img[alt*="verification"]'
        ]
        
        for selector in captcha_selectors:
            try:
                if await self.page.locator(selector).count() > 0:
                    print(f"🎯 Captcha detected with selector: {selector}")
                    return True, selector
            except:
                continue
        
        # Quick check for reCAPTCHA iframes
        try:
            iframes = await self.page.query_selector_all('iframe')
            for iframe in iframes:
                src = await iframe.get_attribute('src')
                if src and ('recaptcha' in src.lower() or 'captcha' in src.lower()):
                    print("🎯 reCAPTCHA iframe detected")
                    return True, 'iframe'
        except:
            pass
        
        return False, None
    
    async def solve_captcha_with_ai(self, captcha_element):
        """Solve captcha using AI vision - optimized"""
        if not self.openai_client:
            return False
        
        try:
            # Take screenshot of captcha
            screenshot = await captcha_element.screenshot()
            
            # Convert to base64
            image_base64 = base64.b64encode(screenshot).decode('utf-8')
            
            # Use OpenAI Vision API with reduced tokens
            response = self.openai_client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Read the text/numbers in this captcha image. Reply with only the answer."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=5  # Reduced from 10
            )
            
            answer = response.choices[0].message.content.strip()
            print(f"🤖 AI solved captcha: {answer}")
            return answer
            
        except Exception as e:
            print(f"❌ AI captcha solving failed: {e}")
            return False
    
    async def handle_text_captcha(self):
        """Handle text-based captcha - optimized"""
        try:
            # Look for captcha input field
            input_selectors = [
                'input[name*="captcha"]',
                'input[id*="captcha"]',
                'input[placeholder*="captcha"]',
                'input[type="text"]'
            ]
            
            captcha_input = None
            for selector in input_selectors:
                if await self.page.locator(selector).count() > 0:
                    captcha_input = selector
                    break
            
            if not captcha_input:
                return False
            
            # Find captcha image
            captcha_detected, captcha_selector = await self.detect_captcha()
            if not captcha_detected:
                return False
            
            # Try AI solving first
            if self.openai_client:
                captcha_element = self.page.locator(captcha_selector).first
                ai_answer = await self.solve_captcha_with_ai(captcha_element)
                if ai_answer:
                    await self.page.fill(captcha_input, ai_answer)
                    return True
            
            # Fallback to manual solving
            print("⚠️ Manual captcha solving required")
            print("Please solve the captcha manually in the browser window.")
            import sys
            try:
                if sys.stdin.isatty():
                    input("Press Enter once you've solved it...")
            except EOFError:
                pass
            return True
            
        except Exception as e:
            print(f"❌ Text captcha handling failed: {e}")
            return False
    
    async def handle_recaptcha(self):
        """Handle reCAPTCHA - optimized"""
        try:
            # Check for reCAPTCHA checkbox
            checkbox_selectors = [
                '.recaptcha-checkbox',
                '[class*="recaptcha-checkbox"]',
                'iframe[src*="recaptcha"]'
            ]
            
            for selector in checkbox_selectors:
                if await self.page.locator(selector).count() > 0:
                    print("⚠️ reCAPTCHA detected - manual intervention required")
                    print("Please complete the reCAPTCHA manually in the browser window.")
                    import sys
                    try:
                        if sys.stdin.isatty():
                            input("Press Enter once you've completed the reCAPTCHA...")
                    except EOFError:
                        pass
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ reCAPTCHA handling failed: {e}")
            return False
    
    async def handle_captcha(self, timeout=5):  # Reduced from 10s
        """Enhanced captcha handling with timeout - optimized"""
        try:
            # Quick check for captcha
            captcha_detected, captcha_type = await self.detect_captcha()
            if not captcha_detected:
                return True
            
            print(f"🎯 Handling {captcha_type} captcha...")
            
            # Handle different types of captcha
            if captcha_type == 'iframe' or 'recaptcha' in captcha_type:
                return await self.handle_recaptcha()
            else:
                return await self.handle_text_captcha()
                
        except Exception as e:
            print(f"❌ Captcha handling error: {e}")
            # Fallback to manual solving
            print("⚠️ Manual captcha solving required")
            import sys
            try:
                if sys.stdin.isatty():
                    input("Press Enter once you've solved the captcha...")
            except EOFError:
                pass
            return True
    
    async def wait_for_captcha_completion(self, timeout=15):  # Reduced from 30s
        """Wait for captcha completion with reduced timeout"""
        try:
            start_time = asyncio.get_event_loop().time()
            while asyncio.get_event_loop().time() - start_time < timeout:
                captcha_detected, _ = await self.detect_captcha()
                if not captcha_detected:
                    return True
                await asyncio.sleep(0.5)
            return False
        except:
            return False