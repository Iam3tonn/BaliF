def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator
    import re
    from datetime import datetime

    def fetch_article_content(url):
        # Отправьте запрос на страницу статьи
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Найдите и извлеките основной текст статьи
        content_section = soup.find('div', class_='content_section wrapper-sections py-3')
        content_text = content_section.get_text(strip=True) if content_section else "Текст статьи не найден."
        
        # Извлечение даты и времени
        date_time_match = re.search(r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}", content_text)
        if date_time_match:
            date_time_str = date_time_match.group()
            # Преобразование даты и времени в желаемый формат
            date_time = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M')
            formatted_date_time = date_time.strftime('%d %B %Y - %H:%M')
        else:
            formatted_date_time = "Дата не указана"
        
        # Удаление даты и времени из текста
        if date_time_match:
            content_text = content_text.replace(date_time_str, '').strip()

        return content_text, formatted_date_time

    def fetch_news_from_telam():
        url = 'https://www.telam.com.ar'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        news_section = soup.find('section', id="_qb1bgr3q3")
        if not news_section:
            return "Раздел новостей не найден."

        news_items = news_section.find_all('div', class_='nota')
        news_list = []

        translator = Translator()

        for item in news_items:
            title_element = item.find('h1') or item.find('h2') or item.find('h3')
            if title_element:
                title = title_element.get_text(strip=True)
                link = title_element.find('a')['href']
                
                # Проверяем, начинается ли ссылка с http/https
                if not link.startswith('http'):
                    full_link = url + '/' + link if not url.endswith('/') else url + link
                else:
                    full_link = link

                title_russian = translator.translate(title, src='es', dest='ru').text
                article_content, date_time = fetch_article_content(full_link)
                
                news_list.append({'title': title_russian, 'link': full_link, 'full_text': article_content, 'date_time': date_time})

        return news_list

    news = fetch_news_from_telam()
    with open('Json files/telam.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=4)

    print("telam завершено")

run()

