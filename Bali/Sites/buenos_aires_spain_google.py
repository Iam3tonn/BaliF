def run():   
    import json
    from GoogleNews import GoogleNews
    from googletrans import Translator
    from datetime import datetime, timedelta
    import re

    # Функция для перевода относительной даты с испанского на английский
    def translate_date_spanish_to_english(date_str, translator):
        translations = {
            'hora': 'hour',
            'horas': 'hours',
            'día': 'day',
            'días': 'days',
            'minuto': 'min',
            'minutos': 'mins'
        }
        for es, en in translations.items():
            if es in date_str:
                return date_str.replace(es, en)
        return date_str

    # Функция для преобразования относительной даты в абсолютную
    def format_relative_date(date_str):
        now = datetime.now()
        if 'hour' in date_str or 'hours' in date_str:
            hours = int(re.search(r'\d+', date_str).group())
            return (now - timedelta(hours=hours)).strftime("%d %B %Y - %H:%M")
        elif 'day' in date_str or 'days' in date_str:
            days = int(re.search(r'\d+', date_str).group())
            return (now - timedelta(days=days)).strftime("%d %B %Y - %H:%M")
        elif 'min' in date_str or 'mins' in date_str:
            minutes = int(re.search(r'\d+', date_str).group())
            return (now - timedelta(minutes=minutes)).strftime("%d %B %Y - %H:%M")
        else:
            return date_str

    # Создание экземпляра GoogleNews и переводчика
    googlenews = GoogleNews(lang='es', period='3d')
    googlenews.search('Buenos Aires')
    translator = Translator()

    # Получение и обработка результатов
    result = googlenews.result()
    news_data = []

    for news in result[:5]:
        translated_title = translator.translate(news['title'], src='es', dest='ru').text
        translated_date = translator.translate(news['date'], src='es', dest='en').text
        translated_date = translate_date_spanish_to_english(translated_date, translator)
        formatted_date = format_relative_date(translated_date)

        news_item = {
            "title": translated_title,
            "date": formatted_date,
            "full_text": news['desc'],
            "link": news['link'],
        }
        news_data.append(news_item)

    # Сохранение данных в JSON файл
    with open('Json files/buenos_aires_spain_google.py.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)
        print("buenos_aires_spain_google выполнен")

run()

