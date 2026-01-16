import requests
from bs4 import BeautifulSoup
import re

class CAAScraper:
    def __init__(self):
        self.url = "https://www.caa.ae/Pages/Institutes/All.aspx"

    def is_valid_university(self, text):
        text = text.strip()
        text_upper = text.upper()

        # 1. Length sanity checks
        if len(text) < 10 or len(text) > 120:
            return False

        # 2. Reject sentence-like content
        if any(p in text for p in [".", "—", "–", ";", ":"]):
            return False

        # 3. Must contain strong academic keywords
        academic_keywords = [
            "UNIVERSITY",
            "COLLEGE",
            "INSTITUTE",
            "ACADEMY",
            "SCHOOL"
        ]
        if not any(k in text_upper for k in academic_keywords):
            return False

        # 4. Reject navigation / editorial keywords
        junk_keywords = [
            "ACCESSIBILITY",
            "SIGN IN",
            "CONTACT",
            "ABOUT",
            "PRIVACY",
            "TERMS",
            "COPYRIGHT",
            "SITEMAP",
            "DISCLAIMER",
            "SETTINGS",
            "FILTER",
            "OPTIONS",
            "MODE",
            "THEME",
            "READING",
            "LINK",
            "LOCATION",
            "KNOWLEDGE",
            "POWER",
            "ECONOMY",
            "SOCIETY",
            "FUTURE"
        ]
        if any(j in text_upper for j in junk_keywords):
            return False

        return True

    def scrape(self):
        print(f"[*] Scraping CAA accredited institutes from {self.url}")
        institutes = set()

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(
                self.url,
                headers=headers,
                verify=False,
                timeout=20
            )
            soup = BeautifulSoup(response.content, "html.parser")

            candidates = soup.find_all(["td", "span", "a", "div"])

            for tag in candidates:
                text = tag.get_text(strip=True)
                if self.is_valid_university(text):
                    institutes.add(text)

        except Exception as e:
            print(f"[!] CAA scraping failed: {e}")

        cleaned = []
        for name in sorted(institutes):
            cleaned.append({
                "name": name,
                "accredited": True,
                "source": "CAA UAE Government",
                "source_url": self.url
            })

        print(f"[*] Final cleaned CAA universities count: {len(cleaned)}")
        return cleaned
