import time
from loguru import logger

from src.browser import BrowserManager
from src.loader import ExhibitorLoader
from src.parser import ExhibitorParser
from src.exporter import Exporter
from src.config import setting

logger.add(setting.base_dir / "logs/scraper_{time}.log", rotation="10 MB", level="DEBUG")


def main():
    logger.info("Scraper initialized!")

    all_results = []

    try:
        with BrowserManager(headless=False) as driver:
            loader = ExhibitorLoader(driver)

            loader.load_all_exhibitors()
            urls = loader.get_exhibitor_urls()

            urls = urls[:50]
            if not urls:
                logger.error("No URLs collected. Terminating process.")
                return

            logger.info(f"Starting parsing for {len(urls)} companies...")

            for index, url in enumerate(urls, 1):
                try:
                    logger.info(f"[{index}/{len(urls)}] Navigating to: {url}")
                    driver.get(url)

                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, 500);")
                    time.sleep(1)

                    parser = ExhibitorParser(driver.page_source)
                    exhibitor_data = parser.parse()

                    if exhibitor_data:
                        all_results.append(exhibitor_data)
                        logger.success(f"Data collected for: {exhibitor_data.company_name}")

                    if index % 50 == 0:
                        Exporter.to_csv(all_results, "backup_exhibitors_list.csv")
                        logger.debug("Periodic backup saved.")

                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")
                    continue

    except KeyboardInterrupt:
        logger.warning("Scraping interrupted by user. Saving partial results...")

    finally:
        if all_results:
            logger.info(f"Total companies collected: {len(all_results)}")
            Exporter.to_csv(all_results, "final_exhibitors_list.csv")
        else:
            logger.error("No data available to save.")


if __name__ == "__main__":
    main()