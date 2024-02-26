def run():
    import requests
    from bs4 import BeautifulSoup
    import json
    from googletrans import Translator
    # URL новостного сайта
    url = "https://www.cronista.com/"

    try:
        # Отправляем запрос на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Парсим HTML-содержимое страницы
            soup = BeautifulSoup(response.content, 'html.parser')

            # Находим все новостные элементы на основе структуры страницы
            news_items = soup.select('div.block article.item.news')

            # Список для хранения данных о новостях
            news_data = []

            # Инициализируем объект переводчика
            translator = Translator()

            # Обрабатываем максимум 10 новостных элементов
            for item in news_items[:10]:
                title = item.find('h2', class_='title').get_text(strip=True) if item.find('h2', class_='title') else 'Нет заголовка'
                link = item.find('a', class_='link')['href'] if item.find('a', class_='link') else 'Нет ссылки'
                
                # Переводим заголовок на русский язык
                translated_title = translator.translate(title, src='auto', dest='ru').text

               # Получаем содержимое каждой новости
                news_response = requests.get(url + link)
                news_soup = BeautifulSoup(news_response.content, 'html.parser')
                news_content = news_soup.find('div', class_='content vsmcontent').get_text(strip=True) if news_soup.find('div', class_='content vsmcontent') else 'Нет содержания'

                # Заменяем двойные кавычки на одинарные в основном тексте
                news_content = news_content.replace('"', "'")

                news_data.append({"title": translated_title, "url": url + link, "content": news_content})

            # Сохраняем данные о новостях в JSON-файл
            with open('Json files/cronista.json', 'w', encoding='utf-8') as json_file:
                json.dump(news_data, json_file, ensure_ascii=False)

            print("Cronista завершено")
        else:
            print("Не удалось получить данные с сайта. Код статуса:", response.status_code)

    except Exception as e:
        print("Произошла ошибка:", e)

run()

if __name__ == "__main__":
    run()
