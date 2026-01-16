import requests
from bs4 import BeautifulSoup
import pandas as pd

class LivingScraper:
    def __init__(self):
        self.url = "https://www.universityliving.com/blog/student-finances/cost-of-living-in-dubai/"

    def scrape(self):
        print(f"[*] Scraping cost of living data from {self.url}")
        result = {
            "source": self.url,
            "scope": "Dubai (Primary student hub in UAE)",
            "data_confidence": "MEDIUM",
            "tables": []
        }

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")

            tables = pd.read_html(str(soup))
            for table in tables:
                table = table.fillna("N/A")
                result["tables"].append(table.to_dict(orient="records"))

            if not result["tables"]:
                result["data_confidence"] = "LOW"

        except Exception as e:
            result["error"] = str(e)
            result["data_confidence"] = "LOW"

        return result
