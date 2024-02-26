import requests
from bs4 import BeautifulSoup
import time

def fetch_infobae_news(timeout_seconds=10, delay_seconds=2):
    url = "https://www.infobae.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    try:
        time.sleep(delay_seconds)
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all('h2', class_='headline__title')
        news = []
        for item in news_items:
            title = item.get_text().strip()
            link = item.find('a')['href']
            news.append({'title': title, 'link': link})
        return news
    except requests.Timeout:
        print("The request timed out")
        return []
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

news = fetch_infobae_news(timeout_seconds=30, delay_seconds=5)
print(news[:5])
