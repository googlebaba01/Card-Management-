# main.py - Reliable E-commerce Automation
import asyncio
import time
import os
from src.browser_manager import AdvancedBrowserManager
from src.platform_detector import PlatformDetector
from src.captcha_handler import CaptchaHandler
from config.settings import PLATFORMS, CREDENTIALS, USER_DETAILS

class ReliableEcommerceAutomation:
    def __init__(self):
        self.browser_manager = AdvancedBrowserManager()
        self.start_time = None

    async def automate_checkout(self, product_url):
        self.start_time = time.time()
        try:
            platform = PlatformDetector.detect_platform(product_url)
            print(f"🎯 Platform detected: {platform}")
            page = await self.browser_manager.start_browser(persistent=True)
            captcha_handler = CaptchaHandler(page)
            print("🚀 Browser started, beginning automation...")
            # Only login if not already logged in
            if not await self.is_logged_in(page):
                login_success = await self.login(page, platform, captcha_handler)
                if not login_success:
                    print("❌ Login failed")
                    return None
            # Go directly to product page
            if not await self.browser_manager.safe_navigate(product_url, timeout=8000):
                print("❌ Failed to load product page")
                return None
            # Add to cart
            cart_success = await self.add_to_cart(page, product_url, captcha_handler)
            if not cart_success:
                print("❌ Add to cart failed")
                return None
            # Go to checkout
            checkout_url = await self.checkout(page, captcha_handler)
            total_time = time.time() - self.start_time
            print(f"✅ Completed in {total_time:.2f} seconds")
            return checkout_url
        except Exception as e:
            print(f"❌ Automation failed: {str(e)}")
            return None
        finally:
            try:
                # Only prompt if running interactively
                import sys
                if sys.stdin.isatty():
                    input("Press Enter to close browser...")
            except EOFError:
                pass
            await self.browser_manager.close_browser()

    async def login(self, page, platform, captcha_handler):
        try:
            print("🔐 Starting login process...")
            login_urls = [
                'https://www.amazon.in/ap/signin',
                'https://www.amazon.in/gp/sign-in.html',
                'https://www.amazon.in'
            ]
            for url in login_urls:
                try:
                    if await self.browser_manager.safe_navigate(url, timeout=15000):
                        await asyncio.sleep(1)
                        if await self.is_logged_in(page):
                            print("✅ Already logged in!")
                            return True
                        # Try to find and click sign-in if on homepage
                        if 'amazon.in' in url and not 'signin' in url:
                            signin_selectors = ['#nav-link-accountList', 'a[data-nav-role="signin"]']
                            for selector in signin_selectors:
                                if await self.browser_manager.element_exists(selector):
                                    await self.browser_manager.human_like_click(selector, fast_mode=True)
                                    await asyncio.sleep(1)
                                    break
                        login_success = await self.perform_login(page, captcha_handler)
                        if login_success:
                            return True
                except Exception as e:
                    print(f"⚠️ Login URL {url} failed: {e}")
                    continue
            return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False

    async def perform_login(self, page, captcha_handler):
        try:
            await captcha_handler.handle_captcha()
            phone_selectors = [
                'input[name="email"]',
                '#ap_email',
                'input[type="tel"]',
                'input[placeholder*="phone"]',
                'input[placeholder*="mobile"]'
            ]
            phone_entered = False
            for selector in phone_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    print(f"📱 Found phone/email field: {selector}")
                    phone_number = CREDENTIALS['amazon'].get('phone', CREDENTIALS['amazon']['email'])
                    await self.browser_manager.human_like_typing(selector, phone_number, fast_mode=True)
                    phone_entered = True
                    break
                except:
                    continue
            if not phone_entered:
                print("❌ Phone/email field not found!")
                return False
            continue_selectors = ['#continue', 'input[id="continue"]', 'button[type="submit"]']
            continue_clicked = False
            for selector in continue_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    await self.browser_manager.human_like_click(selector, fast_mode=True)
                    continue_clicked = True
                    break
                except:
                    continue
            if not continue_clicked:
                await page.keyboard.press('Enter')
            await asyncio.sleep(0.2)
            await captcha_handler.handle_captcha()
            password_selectors = ['#ap_password', 'input[name="password"]', 'input[type="password"]']
            password_entered = False
            for selector in password_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    print(f"🔒 Found password field: {selector}")
                    await self.browser_manager.human_like_typing(selector, CREDENTIALS['amazon']['password'], fast_mode=True)
                    password_entered = True
                    break
                except:
                    continue
            if not password_entered:
                print("❌ Password field not found!")
                return False
            signin_selectors = ['#signInSubmit', 'input[id="signInSubmit"]', 'button[type="submit"]']
            signin_clicked = False
            for selector in signin_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    await self.browser_manager.human_like_click(selector, fast_mode=True)
                    signin_clicked = True
                    break
                except:
                    continue
            if not signin_clicked:
                await page.keyboard.press('Enter')
            await asyncio.sleep(0.5)
            await captcha_handler.handle_captcha()
            return await self.is_logged_in(page)
        except Exception as e:
            print(f"❌ Login performance error: {e}")
            return False

    async def is_logged_in(self, page):
        try:
            login_indicators = [
                '#nav-link-accountList',
                '[data-nav-role="signin"]',
                '#nav-your-account'
            ]
            for indicator in login_indicators:
                if await self.browser_manager.element_exists(indicator):
                    element_text = await page.locator(indicator).text_content()
                    if element_text and ('hello' in element_text.lower() or 'account' in element_text.lower()):
                        print("✅ Login successful!")
                        return True
            current_url = page.url
            if 'signin' not in current_url and 'login' not in current_url:
                print("✅ Login appears successful!")
                return True
            return False
        except Exception as e:
            print(f"⚠️ Login verification error: {e}")
            return False

    async def add_to_cart(self, page, product_url, captcha_handler):
        try:
            print("🛒 Adding product to cart...")
            await asyncio.sleep(0.2)
            await captcha_handler.handle_captcha()
            add_to_cart_selectors = [
                '#add-to-cart-button',
                'input[name="submit.add-to-cart"]',
                '[data-testid="add-to-cart-button"]',
                'button[aria-labelledby*="add-to-cart"]',
                'input[value*="Add to Cart"]',
                'button:has-text("Add to Cart")',
                'input[type="submit"][value*="Cart"]'
            ]
            cart_added = False
            for selector in add_to_cart_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    print(f"🎯 Found add to cart button: {selector}")
                    await self.browser_manager.human_like_click(selector, fast_mode=True)
                    cart_added = True
                    break
                except:
                    continue
            if not cart_added:
                print("❌ Add to cart button not found!")
                return False
            await asyncio.sleep(0.5)
            cart_verified = await self.verify_cart_addition(page)
            if cart_verified:
                print("✅ Product added to cart successfully!")
                return True
            else:
                print("⚠️ Product may not have been added to cart properly")
                return False
        except Exception as e:
            print(f"❌ Add to cart error: {e}")
            return False

    async def verify_cart_addition(self, page):
        try:
            cart_indicators = [
                '#nav-cart-count',
                '[data-testid="cart-count"]',
                '.nav-cart-count',
                'span[class*="cart-count"]'
            ]
            for indicator in cart_indicators:
                if await self.browser_manager.element_exists(indicator):
                    count_text = await page.locator(indicator).text_content()
                    if count_text and count_text.strip() != '0':
                        print(f"✅ Cart count: {count_text}")
                        return True
            success_messages = [
                'Added to Cart',
                'Item added to cart',
                'Successfully added'
            ]
            page_content = await page.content()
            for message in success_messages:
                if message.lower() in page_content.lower():
                    print(f"✅ Found success message: {message}")
                    return True
            return False
        except Exception as e:
            print(f"⚠️ Cart verification error: {e}")
            return False

    async def checkout(self, page, captcha_handler):
        try:
            print("💳 Proceeding to checkout...")
            cart_urls = [
                'https://www.amazon.in/gp/cart/view.html',
                'https://www.amazon.in/cart'
            ]
            cart_accessed = False
            for cart_url in cart_urls:
                try:
                    if await self.browser_manager.safe_navigate(cart_url, timeout=8000):
                        await asyncio.sleep(0.2)
                        cart_items_selectors = [
                            '[data-name="Active Items"]',
                            '.sc-list-item',
                            '.cart-item',
                            '[data-testid="cart-item"]'
                        ]
                        for selector in cart_items_selectors:
                            try:
                                await page.wait_for_selector(selector, timeout=2000)
                                print("✅ Cart has items")
                                cart_accessed = True
                                break
                            except:
                                continue
                        if cart_accessed:
                            break
                except Exception as e:
                    print(f"⚠️ Cart URL {cart_url} failed: {e}")
                    continue
            if not cart_accessed:
                print("❌ No items in cart after add-to-cart. Aborting.")
                return None
            await captcha_handler.handle_captcha()
            checkout_selectors = [
                'input[name="proceedToRetailCheckout"]',
                '[data-testid="proceed-to-checkout-action"]',
                'input[aria-labelledby*="checkout"]',
                'button[aria-labelledby*="checkout"]',
                'input[value*="Proceed to checkout"]',
                'button:has-text("Proceed to checkout")'
            ]
            checkout_clicked = False
            for selector in checkout_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    print(f"🎯 Found checkout button: {selector}")
                    async with page.expect_navigation(timeout=7000):
                        await self.browser_manager.human_like_click(selector, fast_mode=True)
                    # Allow images and CSS on the checkout page
                    await self.browser_manager.allow_all_resources(page)
                    # await page.reload()
                    checkout_clicked = True
                    break
                except:
                    continue
            if not checkout_clicked:
                print("❌ Checkout button not found!")
                return None
            # Wait for checkout page to load
            try:
                await page.wait_for_selector('form[name="addressForm"], input[name="enterAddressFullName"], input[name="add-new-address"]', timeout=5000)
            except:
                pass  # Address form may not always appear
            # If redirected to /ap/signin, perform login again and retry checkout
            current_url = page.url
            if '/ap/signin' in current_url:
                print("🔄 Amazon requires re-authentication at checkout. Logging in again...")
                login_success = await self.login(page, 'amazon', captcha_handler)
                if not login_success:
                    print("❌ Login at checkout failed. Aborting.")
                    return None
                # Try proceeding to checkout again
                for selector in checkout_selectors:
                    try:
                        await page.wait_for_selector(selector, timeout=2000)
                        print(f"🎯 Retrying checkout button: {selector}")
                        async with page.expect_navigation(timeout=7000):
                            await self.browser_manager.human_like_click(selector, fast_mode=True)
                        break
                    except:
                        continue
                await asyncio.sleep(0.5)
                current_url = page.url
            # Autofill address if address form is present
            await self.autofill_amazon_address(page)
            current_url = page.url
            if '/ap/signin' in current_url:
                print("❌ Still stuck at login page after retry. Aborting.")
                return None
            if 'checkout' in current_url:
                print(f"✅ Checkout URL: {current_url}")
                return current_url
            elif 'cart' in current_url:
                print("❌ Redirected back to cart after checkout. Aborting.")
                return None
            else:
                print(f"⚠️ Unexpected checkout URL: {current_url}")
                return current_url
        except Exception as e:
            print(f"❌ Checkout error: {e}")
            return None

    async def autofill_amazon_address(self, page):
        """Autofill Amazon address form if present using USER_DETAILS"""
        try:
            # Wait for address form to appear (if any)
            address_selectors = {
                'name': 'input[name="enterAddressFullName"]',
                'phone': 'input[name="enterAddressPhoneNumber"]',
                'pincode': 'input[name="enterAddressPostalCode"]',
                'address': 'input[name="enterAddressAddressLine1"]',
                'city': 'input[name="enterAddressCity"]',
            }
            # Check if address form is present
            form_present = False
            for key, selector in address_selectors.items():
                if await page.locator(selector).count() > 0:
                    form_present = True
                    break
            if not form_present:
                print("ℹ️ No address form detected (address may already be set)")
                return
            print("✍️ Autofilling address form...")
            # Fill each field if present
            if await page.locator(address_selectors['name']).count() > 0 and USER_DETAILS['name']:
                await page.fill(address_selectors['name'], USER_DETAILS['name'])
            if await page.locator(address_selectors['phone']).count() > 0 and USER_DETAILS['phone']:
                await page.fill(address_selectors['phone'], USER_DETAILS['phone'])
            if await page.locator(address_selectors['pincode']).count() > 0 and USER_DETAILS['pincode']:
                await page.fill(address_selectors['pincode'], USER_DETAILS['pincode'])
            if await page.locator(address_selectors['address']).count() > 0 and USER_DETAILS['address']:
                await page.fill(address_selectors['address'], USER_DETAILS['address'])
            if await page.locator(address_selectors['city']).count() > 0 and USER_DETAILS['city']:
                await page.fill(address_selectors['city'], USER_DETAILS['city'])
            # Submit the address form (look for a continue/save button)
            submit_selectors = [
                'input.a-button-input[name="shipToThisAddress"]',
                'input.a-button-input[name="useSelectedAddress"]',
                'input.a-button-input[type="submit"]',
                'input[type="submit"]',
                'button.a-button-text',
            ]
            for selector in submit_selectors:
                if await page.locator(selector).count() > 0:
                    print(f"🚚 Submitting address form via {selector}")
                    await page.click(selector)
                    await asyncio.sleep(2)
                    break
            print("✅ Address autofill complete!")
        except Exception as e:
            print(f"⚠️ Address autofill error: {e}")
            return

async def main():
    print("🎉 Starting Reliable E-commerce Automation")
    print("=" * 50)
    try:
        product_url = input("Enter Amazon product URL: ").strip()
    except EOFError:
        print("❌ No input available. Please provide the product URL as an argument or via environment variable.")
        return
    if not product_url:
        print("❌ Please provide a valid product URL")
        return
    automation = ReliableEcommerceAutomation()
    checkout_url = await automation.automate_checkout(product_url)
    if checkout_url:
        print(f"\n🎉 SUCCESS! Checkout URL: {checkout_url}")
        print("\n📋 Next steps:")
        print("1. Open the checkout URL in your browser")
        print("2. Verify the product is in your cart")
        print("3. Complete the checkout process")
    else:
        print("\n❌ Automation failed. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())