from pathlib import Path
from dataclasses import dataclass


BASE_DIR = Path(__file__).resolve().parent.parent

EXHIBITORS_URL = "https://www.embedded-world.de/en/exhibitors-products/find-exhibitors"
DOMAIN = "https://www.embedded-world.de"


@dataclass(frozen=True)
class SeleniumConfig:
    headless: bool = False
    window_width: int = 1920
    window_height: int = 1080

    page_load_timeout: int = 60
    implicit_wait: int = 5
    explicit_wait: int = 20

    max_show_more_clicks: int = 200


@dataclass(frozen=True)
class ScraperConfig:

    exhibitors_url: str = EXHIBITORS_URL
    base_dir = BASE_DIR
    domain: str = DOMAIN
    selenium: SeleniumConfig = SeleniumConfig()

    output_dir: Path = BASE_DIR / "data"
    output_csv_name: str = "exhibitors.csv"
    output_xlsx_name: str = "exhibitors.xlsx"

    scroll_pause: float = 2.0


setting = ScraperConfig()