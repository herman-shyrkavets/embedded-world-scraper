import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger
from src.config import setting


class ExhibitorLoader:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, setting.selenium.explicit_wait)

    def load_all_exhibitors(self):
        logger.info(f"Navigating to page: {setting.exhibitors_url}")
        self.driver.get(setting.exhibitors_url)

        self._accept_cookies()

        clicks = 0
        while clicks < setting.selenium.max_show_more_clicks:
            if not self._click_show_more():
                logger.warning("'Show more' button not found or list is complete.")
                break
            clicks += 1
            logger.debug(f"Clicked 'Show more': {clicks}")
            time.sleep(setting.scroll_pause)

        logger.info("Initiating final scrolling (lazy load handling)...")

    def _accept_cookies(self):
        try:
            logger.debug("Waiting for cookie banner...")
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)

            button = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cmpwelcomebtnyes a"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", button)

            logger.success("Cookies accepted successfully")
            time.sleep(2)

        except TimeoutException:
            logger.info("Cookie banner did not appear (possibly already accepted).")
        except Exception as e:
            logger.error(f"Error while accepting cookies: {e}")

    def _click_show_more(self) -> bool:
        try:
            possible_selectors = [
                (By.XPATH,
                 "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more')]"),
                (By.CSS_SELECTOR, ".m-exhibitor-list__load-more"),
                (By.XPATH, "//button[contains(text(), 'Show more')]"),
            ]

            button = None
            for by, selector in possible_selectors:
                try:
                    button = self.wait.until(EC.presence_of_element_located((by, selector)))
                    if button.is_displayed():
                        break
                except TimeoutException:
                    continue

            if not button:
                return False

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", button)
            return True

        except Exception as e:
            logger.debug(f"'Show more' button unavailable: {e}")
            return False

    def get_exhibitor_urls(self) -> List[str]:
        from src.config import DOMAIN

        logger.info("Collecting exhibitor URLs...")
        elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/en/exhibitors/']")

        urls = []
        for el in elements:
            url = el.get_attribute("href")
            if url:
                if DOMAIN in url:
                    urls.append(url)
                elif url.startswith("/"):
                    urls.append(DOMAIN + url)

        unique_urls = list(set(urls))
        logger.success(f"Successfully collected {len(unique_urls)} unique URLs")
        return unique_urls