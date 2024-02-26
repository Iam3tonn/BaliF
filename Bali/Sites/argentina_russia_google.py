def run():   
    import json
    from GoogleNews import GoogleNews
    from googletrans import Translator
    from datetime import datetime, timedelta
    import re

    # Функция для преобразования относительной даты в абсолютную
    def format_relative_date(date_str):
        now = datetime.now()
        hours_match = re.search(r'\d+', date_str)
        if 'час' in date_str or 'часа' in date_str:
            if hours_match:
                hours = int(hours_match.group())
                return (now - timedelta(hours=hours)).strftime("%d %B %Y - %H:%M")
        elif 'дня' in date_str or 'дней' in date_str:
            days_match = re.search(r'\d+', date_str)
            if days_match:
                days = int(days_match.group())
                return (now - timedelta(days=days)).strftime("%d %B %Y - %H:%M")
        elif 'минут' in date_str or 'минуты' in date_str:
            minutes_match = re.search(r'\d+', date_str)
            if minutes_match:
                minutes = int(minutes_match.group())
                return (now - timedelta(minutes=minutes)).strftime("%d %B %Y - %H:%M")
        else:
            # Если формат времени не распознан, возвращаем исходную строку
            return date_str

    # Создание экземпляра GoogleNews и переводчика
    googlenews = GoogleNews(lang='ru', period='3d')
    googlenews.search('Аргентина')
    translator = Translator()

    # Получение и обработка результатов
    result = googlenews.result()
    news_data = []

    for news in result[:5]:
        translated_title = translator.translate(news['title'], src='ru', dest='ru').text
        formatted_date = format_relative_date(news['date'])

        news_item = {
            "title": translated_title,
            "date": formatted_date,
            "full_text": news['desc'],
            "link": news['link'],
        }
        news_data.append(news_item)

    # Сохранение данных в JSON файл
    with open('Json files/argentina_russia_google.py.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
        print("argentina_russia_google выполнен")
run()
