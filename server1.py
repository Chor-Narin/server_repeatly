from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import random
import time, random
from selenium.webdriver.common.action_chains import ActionChains


def test_adsense_loading(url):
    # [User opens website in browser]
    print(f"User opens website: {url}")
    
    # [Browser initializes network request]
    print("Browser initializes network request")
    
    # Set up Chrome options to mimic a real browser
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--window-size=1280,720")  # Reasonable window size
    # Suppress unrelated logs (e.g., TensorFlow, GCM errors)
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Initialize WebDriver
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(" - Resolves URL (DNS)")  # Handled by browser
        print(" - Prepares HTTP headers")  # Handled by Selenium
        print(" - Sets cookies & local storage")  # Handled by browser
        print(" - Checks referrer")  # Selenium sets referrer implicitly
        print(" - Adds User-Agent info")
        
        # [Website HTML/JS loads in browser]
        print("Website HTML/JS loads in browser")
        driver.get(url)
        print(" - HTML content displayed")
        print(" - CSS styles applied")  # Handled by browser
        print(" - JS executed")

        # 👇 Add this line to simulate human-like actions
        simulate_human_behavior(driver)
        
        # Wait for page to load and check for AdSense script
        try:
            adsense_script = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//script[contains(@src, 'adsbygoogle.js')]"))
            )
            print(" - AdSense <script> detected")
        except:
            print("No AdSense script detected. Saving page source for debugging.")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to 'page_source.html'. Ending test.")
            return
        
        # [Browser executes AdSense script]
        print("Browser executes AdSense script")
        # Simulate sending request to AdSense server (handled by browser's JS execution)
        print(" - Sends request to Google AdSense server")
        print("   * User-Agent: " + driver.execute_script("return navigator.userAgent;"))
        print("   * Referrer: " + url)
        cookies = driver.get_cookies()
        print("   * Cookies (Google & site): " + json.dumps(cookies, indent=2))
        print("   * JS runtime environment info: Browser-based")
        # Get window size
        window_size = driver.get_window_size()
        print("   * Browser window/screen size: " + json.dumps(window_size))
        # Navigator flags
        navigator_info = {
            'userAgent': driver.execute_script("return navigator.userAgent;"),
            'webdriver': driver.execute_script("return !!navigator.webdriver;"),
            'chrome': driver.execute_script("return !!window.chrome;"),
        }
        print("   * Navigator / chrome / webdriver flags: " + json.dumps(navigator_info, indent=2))
        
        # [AdSense server performs checks]
        print("AdSense server performs checks")
        # Simulate checks (we can't access server-side logic, so assume based on client-side data)
        is_real_browser = 'Chrome' in navigator_info['userAgent'] or 'Firefox' in navigator_info['userAgent'] or 'Edge' in navigator_info['userAgent']
        is_automated = navigator_info['webdriver']
        is_window_reasonable = 800 <= window_size['width'] <= 1920 and 600 <= window_size['height'] <= 1080
        are_cookies_valid = len(cookies) > 0
        is_known_webview = False  # Assume not
        print(" - Is this a real Chrome/Edge/Firefox? (navigator.chrome, other APIs): " + str(is_real_browser))
        print(" - Is the browser automated? (navigator.webdriver): " + str(is_automated))
        print(" - Is the window size reasonable?: " + str(is_window_reasonable))
        print(" - Are cookies / referrer valid?: " + str(are_cookies_valid))
        print(" - Is it inside a known WebView/embedded browser?: " + str(is_known_webview))
        
        # Branch based on checks
        if is_real_browser and not is_automated and is_window_reasonable and are_cookies_valid and not is_known_webview:
            # [Browser passes checks]
            print("Browser passes checks")
            print("AdSense responds with ad HTML/JS")
            # Wait longer for ad to load, check for ad container or iframe
            try:
                # Try multiple ad-related selectors
                ad_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR, 
                        "ins.adsbygoogle, iframe[src*='googlesyndication.com'], div[id*='google_ads']"
                    ))
                )
                print("Browser inserts ad into page DOM")
                print("User sees the ad in page")
                ad_content = ad_element.get_attribute('outerHTML')
                print("Ad content: " + ad_content[:200] + "..." if len(ad_content) > 200 else ad_content)
                # Save page source for debugging
                with open("ad_page_source.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("Page source with ad saved to 'ad_page_source.html'")
            except:
                print("No ad rendered, placeholder or empty space")
                print("Simulated placeholder: <div>No Ad</div>")
                # Save page source for debugging
                with open("no_ad_page_source.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("Page source saved to 'no_ad_page_source.html'")
        else:
            # [Browser fails checks]
            print("Browser fails checks")
            print("AdSense blocks ad")
            print("No ad rendered, placeholder or empty space")
            print("Simulated placeholder: <div>No Ad</div>")
            with open("failed_checks_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to 'failed_checks_page_source.html'")
        
        # Keep browser open for inspection
        print("Browser will remain open for 60 seconds or until you press Enter...")
        try:
            # Wait for user input or timeout after 60 seconds
            input_timeout = 60
            start_time = time.time()
            while time.time() - start_time < input_timeout:
                try:
                    input("Press Enter to close the browser (or wait 60 seconds): ")
                    break
                except KeyboardInterrupt:
                    break
        except Exception as e:
            print(f"Error during wait: {e}")
        print("Closing browser...")
    
    except Exception as e:
        print(f"Error during test: {e}")
        # Save page source for debugging
        if driver:
            with open("error_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to 'error_page_source.html'")
    finally:
        if driver:
            driver.quit()
            print("Browser closed")

def simulate_human_behavior(driver):
    # Get viewport size to ensure mouse stays within bounds
    window_size = driver.get_window_size()
    max_width = window_size['width']
    max_height = window_size['height']
    print(f"Viewport size: {max_width}x{max_height}")

    # --- SCROLLING ---
    total_scrolls = random.randint(3, 7)  # how many scrolls
    for i in range(total_scrolls):
        scroll_amount = random.randint(200, 600)  # px per scroll
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(1.5, 3.5))  # pause between scrolls

    # --- MOUSE MOVES (Simplified) ---
    try:
        actions = ActionChains(driver)
        # Move to a known safe element (e.g., body) without offset
        body = driver.find_element(By.TAG_NAME, "body")
        actions.move_to_element(body).perform()
        print("Moved mouse to body element")
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"Mouse movement error: {e}")
# Example usage
if __name__ == "__main__":
    website_url = "https://opportunitiescorners.com/fifa-world-cup-volunteer-program/#google_vignette"
    test_adsense_loading(website_url)