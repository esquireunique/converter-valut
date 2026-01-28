from datetime import datetime

import requests


class SimpleAPIClient:

    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru"

    def get_rates(self, date=None):

        try:
            if date:
                year, month, day = date.split('-')
                url = f"{self.base_url}/archive/{year}/{month}/{day}/daily_json.js"
            else:
                url = f"{self.base_url}/daily_json.js"

            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except:
            return None

    def get_currency_names(self):
        data = self.get_rates()
        if data and 'Valute' in data:
            names = {}
            for code, info in data['Valute'].items():
                names[code] = info['Name']
            return names
        return {}


if __name__ == "__main__":
    print("Тест API")

    client = SimpleAPIClient()

    print("1. Текущие курсы:")
    data = client.get_rates()
    if data:
        print(f"Дата: {data.get('Date', 'неизвестно')}")
        for code in ['USD', 'EUR', 'CNY']:
            if code in data.get('Valute', {}):
                rate = data['Valute'][code]['Value']
                print(f"{code}: {rate} руб.")
    else:
        print("Не удалось получить данные")

    print("2. Названия валют:")
    names = client.get_currency_names()
    for code, name in list(names.items())[:5]:
        print(f"{code}: {name}")

    print("Готово")
