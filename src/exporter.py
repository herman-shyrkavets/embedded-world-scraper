import pandas as pd
from typing import List
from loguru import logger
from src.models import Exhibitor

class Exporter:
    @staticmethod
    def to_csv(exhibitors: List[Exhibitor], filename: str = "exhibitors_data.csv"):
        if not exhibitors:
            logger.warning("No data found for export.")
            return

        rows = []
        for ex in exhibitors:
            if not ex.employees:
                rows.append({
                    "Company Name": ex.company_name,
                    "Industry": ex.industry,
                    "Country": ex.country,
                    "Website": ex.website,
                    "Employee Name": "N/A",
                    "Employee Title": "N/A",
                    "Employee Email": "N/A"
                })
            else:
                for emp in ex.employees:
                    rows.append({
                        "Company Name": ex.company_name,
                        "Industry": ex.industry,
                        "Country": ex.country,
                        "Website": ex.website,
                        "Employee Name": emp.full_name,
                        "Employee Title": emp.title,
                        "Employee Email": emp.email
                    })

        df = pd.DataFrame(rows)

        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig', sep=';')
            logger.success(f"Successfully exported data to CSV: {filename}")
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")