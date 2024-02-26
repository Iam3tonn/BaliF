def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator
    from datetime import datetime

    def fetch_news(url):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=30)

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Error during requests to {url} : {e}"

        try:
            soup = BeautifulSoup(response.content, 'html.parser')

            news_items = []
            for article in soup.find_all('article'):
                title = article.find('h2')
                link = article.find('a', href=True)
                if title and link:
                    # Correcting URL concatenation here
                    article_url = link['href']
                    # Ensuring the URL is complete
                    if not article_url.startswith('http'):
                        article_url = url + article_url

                    article_content = fetch_article_content(article_url)
                    news_items.append({'title': title.get_text(), 'link': article_url, 'content': article_content})

            return news_items
        except Exception as e:
            return f"Error parsing the HTML content: {e}"

    def fetch_article_content(url):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            return {"error": f"Error during requests to {url} : {e}"}

        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Извлекаем содержимое статьи
            content_div = soup.find('div', {'class': 'newsType__content news-body-complete news-body-center'})
            if not content_div:
                content_div = soup.find('div', {'class': 'newsType__content news-body-complete'})
            if not content_div:
                content_div = soup.find('div', {'class': 'd-liveEntry__content'})
            
            content = content_div.get_text(strip=True) if content_div else "No content found"

            # Извлекаем дату
            date_time_div = soup.find('div', class_='dateTime')
            if date_time_div:
                iso_date = date_time_div.find('time')['datetime']
                # Преобразуем ISO формат в желаемый формат
                date_time = datetime.fromisoformat(iso_date)
                formatted_date = date_time.strftime("%d %B %Y - %H:%M")
            else:
                formatted_date = "No date found"

            return {"content": content, "date": formatted_date}
        except Exception as e:
            return {"error": f"Error parsing article content: {e}"}

    def save_news_to_json(news, filename):
        translator = Translator()
        try:
            translated_news = []
            for item in news:
                translated_title = translator.translate(item['title'], src='auto', dest='ru').text
                translated_item = {
                    'title': translated_title, 
                    'link': item['link'], 
                    'full_text': item['content'].get('content', ''), 
                    'date': item['content'].get('date', '')
                }
                translated_news.append(translated_item)

            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(translated_news, file, ensure_ascii=False, indent=4)

            return "elconfidencial completed"
        except Exception as e:
            return f"Error in processing: {e}"

    # Example usage
    url = 'https://www.elconfidencial.com'
    news = fetch_news(url)
    if isinstance(news, list):  # Check if news were fetched successfully
        result = save_news_to_json(news, 'Json files/elconfidencial.json')
        print(result)
    else:
        print(news)

run()
