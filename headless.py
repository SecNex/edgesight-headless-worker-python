import time
import threading
import base64

from playwright.sync_api import sync_playwright

from database import Database

class Website:
    def __init__(self, url: str, timeout: int = 5, delay: bool = False, delay_time: int = 2):
        self.__url = url
        self.timeout = timeout
        self.__delay = delay
        self.delay_time = delay_time

    def delay(self):
        if self.__delay:
            print(f"[DELAY] Waiting for {self.delay_time} seconds...")
            time.sleep(self.delay_time)
            print("[DELAY] Finished waiting!")

    @property
    def url(self):
        return self.__url
    

class HeadlessPlayer:
    def __init__(self, websites: list[Website] = [], path: str = "screenshots", again_after: int = 5, database: Database = None):
        self.database = database
        self.websites = websites
        self.path = path
        self.after = again_after
        if not self.database:
            print("[HEADLESS] Database is not set!")
            self.thread = threading.Thread(target=self.start)
            self.thread.daemon = True
            self.thread.start()
        if self.database:
            if self.database.connected:
                print("[HEADLESS] Database is connected!")
                self.get_websites_from_db()

    def add_websites(self, websites: list[Website]):
        self.websites.extend(websites)

    def add_website(self, website: Website):
        self.websites.append(website)

    def remove_website(self, website: Website):
        self.websites.remove(website)

    def get_websites_from_db(self) -> list[Website]:
        websites = self.database.fetch("SELECT * FROM websites")
        __websites = []
        for website in websites:
            __websites.append(Website(website[1], website[2], website[3], website[4]))
        self.websites = __websites
        return __websites

    def screenshot(self, website: Website):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for website in self.websites:
                url_base64 = base64.urlsafe_b64encode(website.url.encode()).decode().replace("=", "")
                print(f"[HEADLESS] Website: {website.url} - {url_base64}")
                page = browser.new_page(viewport={"width": 1920, "height": 1080})
                print(f"[HEADLESS] Loading {website.url}...")
                page.goto(website.url, timeout=website.timeout * 1000, wait_until="domcontentloaded")
                print(f"[HEADLESS] Waiting for {website.url} to load...")
                page.wait_for_load_state("networkidle")
                print(f"[HEADLESS] Finished loading {website.url}!")
                print(f"[HEADLESS] Delaying for {website.url}...")
                website.delay()
                print(f"[HEADLESS] Screenshotting {website.url}...")
                page.screenshot(path=f"{self.path}/{url_base64}.png")
                page.close()
            browser.close()

    def get_screenshot_as_base64(self, website: Website):
        url_base64 = base64.urlsafe_b64encode(website.url.encode()).decode().replace("=", "")
        with open(f"{self.path}/{url_base64}.png", "rb") as file:
            return base64.b64encode(file.read()).decode()

    def start(self):
        while True:
            if self.websites:
                for website in self.websites:
                    self.screenshot(website)
            print(f"[HEADLESS] Waiting for {self.after} seconds...")
            time.sleep(self.after)
            if self.database:
                self.get_websites_from_db()
                