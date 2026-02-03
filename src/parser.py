import base64
from typing import Any

from bs4 import BeautifulSoup
from loguru import logger
from src.models import Employee, Exhibitor


class ExhibitorParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "lxml")

    def parse(self) -> Exhibitor | None:
        try:
            company_stage = self.soup.find("div", {'data-testid': 'company-stage-container'})
            company_details = self.soup.find("div", {'data-testid': 'company-details'})
            company_employees = self.soup.find("div", {'data-testid': 'company-employees'})

            return Exhibitor(
                company_name=self._get_company_name(company_stage),
                industry=self._get_industry(company_details),
                country=self._get_country(company_details),
                website=self._get_website(company_details),
                employees=self._get_employees(company_employees)
            )

        except Exception as e:
            logger.error(f"Ошибка при сборке объекта Exhibitor: {e}")
            return None

    def _get_company_name(self, container) -> str:
        if not container:
            return "Unknown Name"
        tag = container.find("h2", {'data-testid': 'headline'})
        return tag.get_text(strip=True) if tag else "Unknown Name"

    def _get_industry(self, container):
        if not container:
            return "N/A"

        industry_header = container.find("h4", {"data-testid": "company-keywords-2-headline"})
        if not industry_header:
            industry_header = container.find("h4", string=lambda x: x and "Industry" in x)

        if industry_header:
            parent_div = industry_header.find_parent("div")
            if parent_div:
                industry_tags = parent_div.find_all('span', class_='pure-tag')
                return ', '.join(tag.get_text(strip=True) for tag in industry_tags) if industry_tags else "N/A"
        return "N/A"

    def _get_country(self, container) -> str:
        if not container:
            return "N/A"

        contact_header = container.find("h4", {"data-testid": "company-details-contacts-headline"})
        if contact_header:
            parent = contact_header.find_parent("div")
            if parent:
                paragraphs = parent.find_all("p", class_="text-copy-l")
                return paragraphs[-1].get_text(strip=True) if paragraphs else "N/A"
        return "N/A"

    def _get_website(self, container) -> str:
        if not container:
            return "N/A"
        website_link = container.find("a", {"data-testid": "company-details-contacts-website"})
        return website_link.get("href") if website_link else "N/A"

    def _decode_email(self, mailto_link: str) -> str | None:
        if not mailto_link or "mailto:" not in mailto_link:
            return None
        try:
            encoded = mailto_link.replace("mailto:", "")
            return base64.b64decode(encoded).decode("utf-8")
        except Exception:
            return None

    def _get_employees(self, container) -> list[Any]:
        employees_list = []
        if not container:
            return employees_list

        employee_blocks = container.find_all("div", class_="col-span-5")
        for block in employee_blocks:
            name_tag = block.find("div", class_="h4")
            title_tag = block.find("div", class_="mt-1 text-copy-l")
            email_tag = block.find("a", class_="email-address")

            if name_tag:
                email = self._decode_email(email_tag.get("href")) if email_tag else None
                full_name = name_tag.get_text(separator=" ", strip=True)

                title = title_tag.get_text(strip=True) if title_tag else "N/A"

                emp = Employee(
                    full_name=full_name,
                    title=title,
                    email=email,
                )
                employees_list.append(emp)

        return employees_list