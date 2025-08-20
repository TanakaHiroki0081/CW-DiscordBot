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
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find('div', {'id': 'vue-container'})
        if not div or not div.has_attr('data'):
            driver.quit()
            raise Exception('Could not find job data on the page.')
        data = json.loads(div['data'])
        driver.quit()
        jobs = []
        for job in data.get('job_offers', []):
            payment = job.get('hourly_payment') or job.get('fixed_price_payment')
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

def main():
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else input('CrowdWorks URL: ')
    scraper = CrowdWorksScraper(url)
    jobs = scraper.fetch_jobs()
    print(json.dumps(jobs, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main() 