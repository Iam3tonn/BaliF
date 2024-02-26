def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    import re
    from googletrans import Translator
    import dateparser

    def fetch_news(url, max_articles=30):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                print("Failed to retrieve the webpage")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_='news-article')

            news_list = []
            for article in articles[:max_articles]:  # Limiting the number of articles
                news_item = {}

                title = article.find('h1', class_='news-article__title') or article.find('h2', class_='news-article__title')
                if title and title.a:
                    news_item['title'] = title.a.get_text(strip=True)
                    news_item['link'] = title.a['href']  # Changed from 'url' to 'link'

                    article_response = requests.get(news_item['link'], timeout=30)
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    main_text_div = article_soup.find('div', class_='col-12 col-md-8 detail-news__main-column')  # Using the specified selector
                    if main_text_div:
                        news_item['full_text'] = main_text_div.get_text(strip=True)

                if news_item:
                    news_list.append(news_item)

            return news_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def save_to_json(news_list, file_path):
        translator = Translator()
        translated_news_list = []

        # Corrected regex pattern for date
        date_pattern = re.compile(r'\d{1,2} de \w+ \d{4} - \d{2}:\d{2}')

        for news_item in news_list:
            if 'title' in news_item:
                title = news_item['title']
                translated_title = translator.translate(title, src='es', dest='ru').text
                news_item['title'] = translated_title

            if 'full_text' in news_item:
                # Extract and remove date from full_text
                date_search = date_pattern.search(news_item['full_text'])
                if date_search:
                    date_str = date_search.group()
                    parsed_date = dateparser.parse(date_str, languages=['es'])
                    if parsed_date:
                        formatted_date = parsed_date.strftime('%d %B %Y - %H:%M')
                        news_item['date'] = formatted_date
                    # Remove the date line from full_text
                    news_item['full_text'] = news_item['full_text'].replace(date_search.group(), '', 1).strip()

            translated_news_list.append(news_item)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(translated_news_list, f, ensure_ascii=False, indent=4)
    url = "https://www.ambito.com"
    news = fetch_news(url)
    save_to_json(news, 'Json files/ambito.json')

    print("ambito completed")
    
run()
