import requests
from bs4 import BeautifulSoup
import json
from googletrans import Translator
from datetime import datetime

def translate_spanish_to_russian(text):
    translator = Translator()
    try:
        translated_text = translator.translate(text, src='es', dest='ru').text
    except Exception as e:
        print(f"Error during translation: {e}")
        translated_text = text
    return translated_text

from datetime import datetime

def get_article_content(article_url):
    base_url = "https://tn.com.ar"
    full_url = base_url + article_url
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article_content = soup.find('div', class_='default-article-color article__body article__article')
            # Extracting and formatting the date
            date_element = soup.find('time', class_='time__container')
            if date_element:
                date_string = date_element['datetime']
                parsed_date = datetime.fromisoformat(date_string)
                formatted_date = parsed_date.strftime("%d %B %Y - %H:%M")
            else:
                formatted_date = "No date found"
            return article_content.text.strip() if article_content else "No content found", formatted_date
        else:
            return "Failed to fetch article", "No date found"
    except Exception as e:
        return f"Error fetching article: {e}", "No date found"

def run():
    base_url = "https://tn.com.ar"
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_containers = soup.find_all('div', class_='brick-container', limit=15)
        news_list = []

        for container in news_containers:
            if container.find('a'):
                relative_link = container.find('a')['href']
                full_link = base_url + relative_link
                news_title_spanish = container.find('h2').text.strip()
                news_title_russian = translate_spanish_to_russian(news_title_spanish)
                article_content, article_date = get_article_content(relative_link)

                news_dict = {
                    "title": news_title_russian,
                    "link": full_link,
                    "full_text": article_content,
                    "date": article_date
                }
                news_list.append(news_dict)

        with open('Json files/tn.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_list, json_file, ensure_ascii=False, indent=4)

        print("tn completed")
    else:
        print("Failed to connect to the website.")

run()

