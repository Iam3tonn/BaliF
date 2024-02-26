def run():    
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator
    from datetime import datetime

    def scrape_articles():
        url = 'https://buenosairesherald.com'
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        articles = soup.find_all('article')
        articles_data = []
        translator = Translator()

        for article in articles:
            title = article.find('h2', class_='penci-entry-title').get_text(strip=True)
            link = article.find('a')['href']
            translated_title = translator.translate(title, src='en', dest='ru').text

            # Make a request to the article's individual link
            article_response = requests.get(link)
            article_data = article_response.text
            article_soup = BeautifulSoup(article_data, 'html.parser')

            # Find and extract the main text
            main_text = article_soup.find('div', class_='post-entry blockquote-style-2').get_text(strip=True)

            # Extract the date and reformat it
            date_element = article_soup.find('time', class_='entry-date published')
            if date_element:
                date_text = date_element.get_text(strip=True)
                date_obj = datetime.strptime(date_text, '%B %d, %Y')
                formatted_date = date_obj.strftime('%d %B, %Y')
            else:
                formatted_date = 'No date available'

            articles_data.append({'title': translated_title, 'link': link, 'full_text': main_text, 'date': formatted_date})

        # Save the data to a JSON file
        with open('Json files/buenosairesherald.json', 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=4)

        print("buenosairesherald completed")

    scrape_articles()



run()
