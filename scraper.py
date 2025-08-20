import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class CrowdWorksScraper:
    def __init__(self, url):
        self.url = url

    def fetch_jobs(self):
        options = Options()
        options.add_argument('--headless')
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find('div', {'id': 'vue-container'})
        if not div or not div.has_attr('data'):
            driver.quit()
            raise Exception('Could not find job data on the page.')
        data_str = div['data']
        try:
            data = json.loads(data_str)
        except Exception:
            data = json.loads(data_str.replace("'", '"'))
        driver.quit()
        jobs = []
        for item in data.get('searchResult', {}).get('job_offers', []):
            job = item.get('job_offer', {})
            payment = item.get('payment', {}).get('hourly_payment') or item.get('payment', {}).get('fixed_price_payment')
            jobs.append({
                'id': job.get('id'),
                'title': job.get('title'),
                'skills': job.get('skills'),
                'status': job.get('status'),
                'payment': payment,
                'last_released_at': job.get('last_released_at'),
                'link': f"https://crowdworks.jp/public/jobs/{job.get('id')}"
            })
        return jobs

if __name__ == '__main__':
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://crowdworks.jp/public/jobs/search?category_id=226&order=new"
    try:
        scraper = CrowdWorksScraper(url)
        jobs = scraper.fetch_jobs()
        print("=== Extracted CrowdWorks Job Data ===")
        for job in jobs:
            print(json.dumps(job, ensure_ascii=False, indent=2))
        if not jobs:
            print("No jobs found.")
    except Exception as e:
        print(f"Error extracting data: {e}") 