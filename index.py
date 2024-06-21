import time
import base64

from playwright.sync_api import sync_playwright

class Website:
    def __init__(self, url: str, timeout: int = 5, delay: bool = False, delay_time: int = 2):
        self.url = url
        self.timeout = timeout
        self.delay = delay
        self.delay_time = delay_time

    def delay(self):
        if self.delay:
            time.sleep(self.delay_time)

    def get(self):
        self.delay()
        return f"Getting {self.url} with timeout {self.timeout}..."
    

class Screenshotter:
    def __init__(self, websites: list[Website], path: str = "screenshots") -> None:
        self.websites = websites
        self.path = path

    def load(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for website in self.websites:
                url_base64 = base64.urlsafe_b64encode(website.url.encode()).decode().replace("=", "")
                page = browser.new_page(viewport={"width": 1920, "height": 1080})
                page.goto(website.url, timeout=website.timeout * 1000, wait_until="domcontentloaded")
                page.wait_for_load_state("networkidle")
                page.screenshot(path=f"{self.path}/{url_base64}.png")
                page.close()
            browser.close()

def main():
    websites = [
        Website("https://www.google.com", timeout=10, delay=True, delay_time=2),
        Website("https://www.bing.com", timeout=50, delay=True, delay_time=1)
    ]
    screenshotter = Screenshotter(websites)
    screenshotter.load()

if __name__ == "__main__":
    main()