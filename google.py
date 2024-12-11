import requests
from bs4 import BeautifulSoup
from rich import print
import time
from dotenv import load_dotenv
import os


class GoogleScraper:
    def __init__(self):
        self.BASE_URL = "https://www.google.com/search"
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'document',
            'Priority': 'u=0, i'
        }
        load_dotenv()
        username = os.getenv('SMARTPROXY_USERNAME')
        password = os.getenv('SMARTPROXY_PASSWORD')
        proxy = f"http://{username}:{password}@dc.smartproxy.com:10000"
        self.proxies = {"http": proxy, "https": proxy}

    def search(self, query: str, linkedin: bool = False, keep_results: bool = True) -> dict:
        print(f'[+] Searching for {query}...')
        soup = self.make_request(query)
        data = {
            'query': query,
            'results': self.extract_results(soup),
            'business_info': self.extract_business_info(query, soup, linkedin)
        }
        if data['results']:
            data['business_info']['website'] = data['results'][0]['link'].split('//')[-1].split('/')[0]
        if not keep_results:
            data['results'] = None
        print('    Total datapoints extracted:', len([x for x in data['business_info'] if data['business_info'][x]]))
        return data

    def make_request(self, query: str) -> BeautifulSoup:
        _query = query.replace(' ', '+').replace('&', '%26')
        url = f"https://www.google.com/search?client=safari&rls=en&q={_query}&ie=UTF-8&oe=UTF-8"
        response = requests.get(url, headers=self.headers, proxies=self.proxies)
        if response.status_code != 200:
            print(f"   Failed to fetch results for {url}")
            time.sleep(2)
            return self.make_request(query)
        return BeautifulSoup(response.text, 'html.parser')

    def extract_business_info(self, query, soup, linkedin: bool = False):
        business_info = soup.find('div', class_='kp-wholepage')
        info = {}
        if business_info:
            info = {
                'query': query,
                'title': business_info.find('div', {'data-attrid': "title"}).text if business_info.find('div', {'data-attrid': "title"}) else None,
                'subtitle': business_info.find('div', {'data-attrid': 'subtitle'}).text if business_info.find('div', {'data-attrid': 'subtitle'}) else None,
                'description': business_info.find('div', {'data-attrid': "VisualDigestDescription"}).text.split('\xa0')[0] if business_info.find('div', {'data-attrid': "VisualDigestDescription"}) else None,
                'owners': business_info.find('div', {'data-attrid': "kc:/business/asset:owner"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "kc:/business/asset:owner"}) else None,
                'founders': business_info.find('div', {'data-attrid': "kc:/business/business_operation:founder"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "kc:/business/business_operation:founder"}) else None,
                'headquarters': business_info.find('div', {'data-attrid': "kc:/organization/organization:headquarters"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "kc:/organization/organization:headquarters"}) else None,
                'founded': business_info.find('div', {'data-attrid': "kc:/organization/organization:founded"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "kc:/organization/organization:founded"}) else None,
                'subsidiaries': business_info.find('div', {'data-attrid': "hw:/collection/organizations:subsidiaries"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "hw:/collection/organizations:subsidiaries"}) else None,
                'employees count': business_info.find('div', {'data-attrid': "ss:/webfacts:number_of_employe"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "ss:/webfacts:number_of_employe"}) else None,
                'CEO': business_info.find('div', {'data-attrid': "kc:/organization/organization:ceo"}).text.split(':')[-1] if business_info.find('div', {'data-attrid': "kc:/organization/organization:ceo"}) else None,
            }

            if business_info.find('div', {'data-attrid': "VisualDigestDescription"}):
                info['wikipedia'] = business_info.find('div', {'data-attrid': "VisualDigestDescription"}).find('a')['href']

            if business_info.find('div', {'data-attrid': "kc:/common/topic:social media presence"}):
                for social_media in business_info.find('div', {'data-attrid': "kc:/common/topic:social media presence"}).find_all('a'):
                    platform = social_media.text.strip().title()
                    info[platform] = social_media['href']

            for key in info:
                if info[key]:
                    info[key] = info[key].split('·')[0].strip()

        if linkedin and 'Linkedin' not in info:
            print('    Searching for Linkedin page...')
            info['Linkedin'] = self.get_company_linkedin(query)
        return info
    
    def extract_results(self, soup):
        results = []
        for result in soup.find_all('div', class_='g'):
            try:
                link = result.find('a', href=True)['href']
                title = result.find('h3').text
                results.append({
                    'title': title,
                    'link': link
                })
            except Exception:
                pass
        return results
    
    def get_company_linkedin(self, query: str):
        query = query + ' site:linkedin.com/company/ austria'
        soup = self.make_request(query)
        results = self.extract_results(soup)
        for result in results:
            if 'linkedin' in result['link']:
                return result['link'].split('?')[0]


if __name__ == '__main__':
    google = GoogleScraper()
    data = google.search("Strabag SE", linkedin=True)