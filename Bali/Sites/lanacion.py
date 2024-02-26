def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator  # Установите библиотеку googletrans: pip install googletrans==4.0.0-rc1

    def fetch_section_news(url, section_class):
        try:
            response = requests.get(url, timeout=30)  # Увеличьте значение timeout, если необходимо
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the specific section by its class
            section = soup.find('section', {'class': section_class})
            if not section:
                return "Section not found."

            # Find all articles within the section
            articles = section.find_all('article')
            
            news = []
            translator = Translator()
            for article in articles:
                title = article.find(['h1', 'h2', 'h3'])
                link = article.find('a', href=True)
                if title and link:
                    title_text = title.get_text(strip=True)
                    
                    # Переводим заголовок на русский язык
                    translation = translator.translate(title_text, src='auto', dest='ru')
                    
                    news.append({  
                        'title': translation.text,
                        'link': 'https://www.lanacion.com.ar' + link['href']
                    })

            return news

        except requests.RequestException as e:
            return f"Error fetching news: {e}"

    # URL of the news site and the specific section class
    url = "https://www.lanacion.com.ar"
    section_class = "open-container lay-container"

    # Fetch the news
    news_data = fetch_section_news(url, section_class)

    # Save to JSON file using UTF-8 encoding
    if isinstance(news_data, list):
        with open('Json files/lanacion.json', 'w', encoding='utf-8') as json_file:
            json.dump(news_data, json_file, ensure_ascii=False, indent=4)
        print("lanacion completed")
    else:
        print("Error occurred: " + news_data)

run()
