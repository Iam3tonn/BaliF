def run():   
    import json
    from GoogleNews import GoogleNews
    from googletrans import Translator
    from datetime import datetime, timedelta
    import re
    from babel.dates import format_datetime

    def format_relative_date(date_str):
        now = datetime.now()
        if 'час' in date_str or 'часа' in date_str:
            hours = int(re.search(r'\d+', date_str).group())
            date_obj = now - timedelta(hours=hours)
        elif 'дня' in date_str or 'дней' in date_str:
            days = int(re.search(r'\d+', date_str).group())
            date_obj = now - timedelta(days=days)
        elif 'минут' in date_str or 'минуты' in date_str:
            minutes = int(re.search(r'\d+', date_str).group())
            date_obj = now - timedelta(minutes=minutes)
        elif 'неделю' in date_str:
            date_obj = now - timedelta(weeks=1)
        else:
            return date_str

        # Форматирование даты и времени на английском языке
        return format_datetime(date_obj, format='d MMMM yyyy - HH:mm', locale='en')

    googlenews = GoogleNews(lang='ru', period='3d')
    googlenews.search('Буэнос Айрес')
    translator = Translator()

    result = googlenews.result()
    news_data = []

    for news in result[:5]:
    # Check if the date is None
        if news['date'] is not None:
            translated_title = translator.translate(news['title'], src='ru', dest='ru').text
            formatted_date = format_relative_date(news['date'])

            news_item = {
                "title": translated_title,
                "date": formatted_date,
                "full_text": news['desc'],
                "link": news['link'],
            }
            news_data.append(news_item)

    with open('Json files/buenos_aires_russia_google.py.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
        print("buenos_aires_russia_google выполнен")

run()


