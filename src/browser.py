from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_driver(
    headless: bool = True,
    window_width: int = 1920,
    window_height: int = 1080,
    page_load_timeout: int = 60,
    implicit_wait: int = 5,
    ) -> WebDriver:

    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"--window-size={window_width},{window_height}")

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.set_page_load_timeout(page_load_timeout)
    driver.implicitly_wait(implicit_wait)

    return driver


class BrowserManager:

    def __init__(
        self,
        headless: bool = True,
        window_width: int = 1920,
        window_height: int = 1080,
        page_load_timeout: int = 60,
        implicit_wait: int = 5,
    ):

        self.headless = headless
        self.window_width = window_width
        self.window_height = window_height
        self.page_load_timeout = page_load_timeout
        self.implicit_wait = implicit_wait
        self.driver: Optional[WebDriver] = None

    def __enter__(self) -> WebDriver:
        self.driver = create_chrome_driver(
            headless=self.headless,
            window_width=self.window_width,
            window_height=self.window_height,
            page_load_timeout=self.page_load_timeout,
            implicit_wait=self.implicit_wait,
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
