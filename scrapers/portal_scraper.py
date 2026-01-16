import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class PortalScraper:
    def __init__(self):
        self.url = "https://www.bachelorsportal.com/search/universities/bachelor/united-arab-emirates"

    def _driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def scrape(self):
        print(f"[*] Scraping course data from BachelorsPortal")
        university_map = {}
        driver = None

        try:
            driver = self._driver()
            driver.get(self.url)
            time.sleep(5)

            for _ in range(3):  # controlled pagination
                cards = driver.find_elements(By.XPATH, "//article | //div[contains(@class,'card')]")

                for card in cards:
                    try:
                        uni = card.text.split("\n")[0]
                        title = card.text.split("\n")[1]

                        course = {
                            "course_name": title,
                            "tuition_fee": "N/A",
                            "duration": "N/A",
                            "source": "BachelorsPortal",
                            "data_confidence": "MEDIUM"
                        }

                        university_map.setdefault(uni, []).append(course)
                    except:
                        continue

                try:
                    driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()
                    time.sleep(3)
                except:
                    break

        except Exception as e:
            print(f"[!] BachelorsPortal scraping failed: {e}")
            print("[*] Returning empty dataset - Chrome may not be available in this environment")

        finally:
            if driver:
                driver.quit()

        return university_map
