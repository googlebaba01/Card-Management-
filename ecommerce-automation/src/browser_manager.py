from playwright.async_api import async_playwright
import asyncio
import random
import time
import pathlib

class AdvancedBrowserManager:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        self.context = None
    
    async def start_browser_ultra_fast(self):
        """Start browser with ultra-optimized settings for maximum speed"""
        self.playwright = await async_playwright().start()
        
        # Ultra-fast browser arguments
        browser_args = [
            '--no-first-run',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-field-trial-config',
            '--disable-ipc-flooding-protection',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--mute-audio',
            '--no-default-browser-check',
            '--safebrowsing-disable-auto-update',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--ignore-certificate-errors-spki-list',
            '--start-maximized',
            '--disable-logging',
            '--disable-logging-redirect',
            '--disable-breakpad',
            '--disable-component-extensions-with-background-pages',
            '--disable-client-side-phishing-detection',
            '--disable-default-apps',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-domain-reliability',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--no-default-browser-check',
            '--no-first-run',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI,BlinkGenPropertyTrees',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-background-timer-throttling',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--mute-audio',
            '--no-default-browser-check',
            '--safebrowsing-disable-auto-update',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--ignore-certificate-errors-spki-list',
            '--start-maximized'
        ]
        
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # Keep visible for debugging
            args=browser_args,
            timeout=30000  # Reduced timeout for faster startup
        )
        
        # Create context with ultra-fast settings
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='Asia/Kolkata',
            permissions=['geolocation'],
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        self.page = await self.context.new_page()
        
        # Ultra-fast anti-detection scripts
        await self.page.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Mock chrome runtime
            if (typeof chrome !== 'undefined') {
                Object.defineProperty(chrome, 'runtime', {
                    get: () => ({
                        onConnect: undefined,
                        onMessage: undefined,
                        connect: undefined,
                        sendMessage: undefined
                    })
                });
            }
            
            // Override permissions
            const originalGetUserMedia = navigator.mediaDevices.getUserMedia;
            navigator.mediaDevices.getUserMedia = function(constraints) {
                return Promise.reject(new Error('Not allowed'));
            };
        """)
        
        # Ultra-fast timeouts
        self.page.set_default_timeout(8000)  # 8 seconds
        self.page.set_default_navigation_timeout(8000)
        
        return self.page
    
    async def start_browser(self, persistent: bool = True):
        """Start browser with enhanced anti-detection measures. Persistent context by default."""
        self.playwright = await async_playwright().start()
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        browser_args = [
            '--no-first-run',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-field-trial-config',
            '--disable-ipc-flooding-protection',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--mute-audio',
            '--no-default-browser-check',
            '--safebrowsing-disable-auto-update',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--ignore-certificate-errors-spki-list',
            '--start-maximized'
        ]
        if persistent:
            user_data_dir = str(pathlib.Path('user_data').absolute())
            self.browser = await self.playwright.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,  # VISIBLE for reliability
                args=browser_args,
                viewport={'width': 1920, 'height': 1080},
                user_agent=random.choice(user_agents),
                locale='en-US',
                timezone_id='Asia/Kolkata',
                permissions=['geolocation'],
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
            )
            self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
            await self._block_resources(self.page)
        else:
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # VISIBLE for reliability
                args=browser_args,
                timeout=60000
            )
            self.context = await self.browser.new_context(
                user_agent=random.choice(user_agents),
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
                timezone_id='Asia/Kolkata',
                permissions=['geolocation'],
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
            )
            self.page = await self.context.new_page()
            await self._block_resources(self.page)
        # Enhanced anti-detection scripts
        await self.page.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            // Mock chrome runtime
            if (typeof chrome !== 'undefined') {
                Object.defineProperty(chrome, 'runtime', {
                    get: () => ({
                        onConnect: undefined,
                        onMessage: undefined,
                        connect: undefined,
                        sendMessage: undefined
                    })
                });
            }
            // Override permissions
            const originalGetUserMedia = navigator.mediaDevices.getUserMedia;
            navigator.mediaDevices.getUserMedia = function(constraints) {
                return Promise.reject(new Error('Not allowed'));
            };
        """)
        self.page.set_default_timeout(3000)
        self.page.set_default_navigation_timeout(3000)
        return self.page
    
    async def _block_resources(self, page):
        """Block images for speed, but allow fonts/media for reliability."""
        async def route_handler(route):
            if route.request.resource_type == "image":
                await route.abort()
            else:
                await route.continue_()
        await page.route("**/*", route_handler)
    
    async def ultra_fast_typing(self, selector, text):
        """Ultra-fast typing with minimal delays"""
        try:
            await self.page.click(selector, timeout=3000)
            await asyncio.sleep(0.05)  # Minimal delay
            
            # Clear and fill
            await self.page.fill(selector, '')
            await self.page.type(selector, text, delay=5)  # Very fast typing
        except Exception as e:
            print(f"⚠️ Ultra-fast typing error: {e}")
            # Fallback to simple fill
            await self.page.fill(selector, text)
    
    async def ultra_fast_click(self, selector):
        """Ultra-fast click with minimal delays"""
        try:
            await asyncio.sleep(0.1)  # Minimal delay
            await self.page.click(selector, timeout=3000)
            await asyncio.sleep(0.1)  # Minimal delay
        except Exception as e:
            print(f"⚠️ Ultra-fast click error: {e}")
            # Try alternative click method
            try:
                await self.page.locator(selector).click(timeout=3000)
            except:
                print(f"❌ Failed to click: {selector}")
    
    async def human_like_typing(self, selector, text, fast_mode=False):
        """Type text with human-like delays (faster in fast mode)"""
        try:
            await self.page.click(selector, timeout=5000)
            await asyncio.sleep(random.uniform(0.05, 0.15) if fast_mode else random.uniform(0.1, 0.3))
            
            # Clear field first
            await self.page.fill(selector, '')
            
            if fast_mode:
                # Fast typing for better performance
                await self.page.type(selector, text, delay=random.uniform(10, 30))
            else:
                # Human-like typing
                for char in text:
                    await self.page.keyboard.type(char)
                    await asyncio.sleep(random.uniform(0.05, 0.15))
        except Exception as e:
            print(f"⚠️ Typing error: {e}")
            # Fallback to simple fill
            await self.page.fill(selector, text)
    
    async def human_like_click(self, selector, fast_mode=False):
        """Click with human-like delay (faster in fast mode)"""
        try:
            await asyncio.sleep(random.uniform(0.2, 0.5) if fast_mode else random.uniform(0.5, 1.5))
            await self.page.click(selector, timeout=5000)
            await asyncio.sleep(random.uniform(0.2, 0.5) if fast_mode else random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"⚠️ Click error: {e}")
            # Try alternative click method
            try:
                await self.page.locator(selector).click(timeout=5000)
            except:
                print(f"❌ Failed to click: {selector}")
    
    async def random_mouse_movement(self):
        """Add random mouse movements"""
        try:
            for _ in range(random.randint(1, 2)):  # Reduced movements for speed
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                await self.page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.05, 0.2))
        except:
            pass  # Ignore mouse movement errors
    
    async def wait_for_element(self, selector, timeout=10000):
        """Wait for element with timeout"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except:
            return False
    
    async def element_exists(self, selector):
        """Check if element exists"""
        try:
            return await self.page.locator(selector).count() > 0
        except:
            return False
    
    async def safe_navigate(self, url, timeout=12000):
        """Navigate to URL with error handling"""
        try:
            await self.page.goto(url, wait_until='domcontentloaded', timeout=timeout)
            return True
        except Exception as e:
            print(f"⚠️ Navigation error: {e}")
            try:
                # Fallback to networkidle
                await self.page.goto(url, wait_until='networkidle', timeout=timeout)
                return True
            except:
                return False
    
    async def close_browser(self):
        """Close browser and cleanup"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"⚠️ Browser close error: {e}")
    
    async def allow_all_resources(self, page):
        """Remove all resource blocking so images and CSS are loaded."""
        # Remove all routes to stop blocking
        await page.unroute("**/*")