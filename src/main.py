import os
from datetime import datetime, timedelta

import requests


class ConverterValut:

    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru"
        self.cache = {}

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("=" * 30)
        print("      КОНВЕРТЕР ВАЛЮТ 😎")
        print("=" * 30)

    def show_menu(self):
        self.clear_screen()
        self.print_header()
        print("            Меню ")
        print("1. Текущий курс валют")
        print("2. Конвертация валют")
        print("3. История курса валюты")
        print("4. Выйти ")
        print("=" * 30)

    def get_choice(self):
        while True:
            choice = input("\nВведите (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            print("Такой цифры для выбора нет")

    def wait_for_enter(self):
        input("\nНажмите Enter для продолжения..")

    def get_rates(self, date=None):
        try:
            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                url = f"{self.base_url}/archive/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}/daily_json.js"
            else:
                url = f"{self.base_url}/daily_json.js"
            cache_key = url
            if cache_key in self.cache:
                return self.cache[cache_key]

            response = requests.get(url, timeout=5)
            data = response.json()

            self.cache[cache_key] = data
            return data
        except Exception as e:
            print("Ошибка")
            return None

    def knopka1_show_rates(self):
        self.clear_screen()
        print("=" * 30)
        print("      ТЕКУЩИЕ КУРСЫ ВАЛЮТ")
        print("=" * 30)
        print("\nЗагрузка данных")

        data = self.get_rates()

        date = data.get('Date', 'неизвестно')
        print(f"\nДата: {date}")
        print("=" * 30)

        currencies = {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'JPY': 'Японская иена',
            'CNY': 'Китайский юань'
        }

        print("\nОсновные валюты:")
        print("=" * 30)

        for code, name in currencies.items():
            if code in data.get('Valute', {}):
                rate = data['Valute'][code]['Value']
                print(f"{code} ({name}): {rate:.2f} руб.")
        print("=" * 30)

        answer = input("\nПосмотреть все валюты (да/нет): ").strip().lower()
        if answer in ['да']:
            self.show_all_currencies(data)

    def show_all_currencies(self, data):
        self.clear_screen()
        print("=" * 30)
        print("      ВСЕ ДОСТУПНЫЕ ВАЛЮТЫ")
        print("=" * 30)

        valute = data.get('Valute', {})
        print(f"\nВсего валют: {len(valute)}")
        print("-" * 30)
        all_codes = list(valute.keys())
        total = len(all_codes)

        shown = 0
        while shown < total:
            self.clear_screen()
            print(f"Валюты {shown+1}-{min(shown+10, total)} из {total}:")
            print("=" * 30)

            for i in range(shown, min(shown+10, total)):
                code = all_codes[i]
                currency = valute[code]
                name = currency['Name']
                rate = currency['Value']
                print(f"{code}: {rate:.4f} руб. - {name}")

            shown += 10

            if shown < total:
                input(f"\nНажмите Enter чтобы увидеть еще (осталось {total-shown})...")
            else:
                print("\n" + "=" * 30)
                print("Это все валюты")

    def knopka2_convert(self):
        self.clear_screen()
        print("=" * 30)
        print("      КОНВЕРТАЦИЯ ВАЛЮТ")
        print("=" * 30)

        while True:
            try:
                amount = float(input("\nСумма для конвертации: ").strip())
                if amount <= 0:
                    print("Сумма должна быть больше 0")
                    continue
                break
            except:
                print("Введите число")

        print("\nПримеры кодов валют: USD, EUR, JPY")
        from_currency = input("Из какой валюты? (код): ").strip().upper()

        to_currency = input("В какую валюту? (код): ").strip().upper()

        print("\nНа какую дату? Оставить пустым, если на сегодня")
        print("Формат: ГГГГ-ММ-ДД (например: 2026-01-25)")
        date_input = input("Дата: ").strip()

        if date_input:
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                date = date_input
            except:
                print("Неправильный формат даты, использую сегодняшнюю дату")
                date = None
        else:
            date = None

        print("\nПолучение данных")
        data = self.get_rates(date)

        if not data:
            print("Не удаось получить курсы валют")
            self.wait_for_enter()
            return

        valute = data.get('Valute', {})

        if from_currency not in valute and from_currency != 'RUB':
            print(f"Валюта {from_currency} не найдена")
            self.wait_for_enter()
            return

        if to_currency not in valute and to_currency != 'RUB':
            print(f"Валюта {to_currency} не найдена")
            self.wait_for_enter()
            return

        if from_currency == 'RUB':
            from_rate = 1.0
        else:
            from_rate = valute[from_currency]['Value']

        if to_currency == 'RUB':
            to_rate = 1.0
        else:
            to_rate = valute[to_currency]['Value']

        amount_in_rub = amount * from_rate
        result = amount_in_rub / to_rate

        self.clear_screen()
        print("=" * 30)
        print("      РЕЗУЛЬТАТ КОНВЕРТАЦИИ")
        print("=" * 30)

        print(f"\n  {amount} {from_currency} = {result:.2f} {to_currency}")
        print("-" * 30)

        date_str = data.get('Date', 'сегодня')
        print(f"\nКурсы на {date_str}:")
        print(f"1 {from_currency} = {from_rate:.4f} RUB")
        print(f"1 {to_currency} = {to_rate:.4f} RUB")

        direct_rate = from_rate / to_rate
        print(f"1 {from_currency} = {direct_rate:.4f} {to_currency}")

        print("\n" + "=" * 30)
        self.wait_for_enter()

    def knopka3_history(self):
        self.clear_screen()
        print("=" * 30)
        print("      ИСТОРИЯ КУРСА ВАЛЮТЫ")
        print("=" * 30)

        print("Выбор валюты")
        print("Примеры: USD, EUR, CNY")

        currency = input("Код валюты: ").strip().upper()

        while True:
            try:
                days = int(input("\nЗа сколько дней? (от 1 до 30): ").strip())
                if 1 <= days <= 30:
                    break
                else:
                    print("Введите число от 1 до 30")
            except:
                print("Введите целое число")

        print(f"\nСбор истории за {days} дней")

        history = []
        today = datetime.now()

        for i in range(days):
            current_date = today - timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")

            if current_date.weekday() >= 5:
                continue

            try:
                data = self.get_rates(date_str)
                if data and currency in data.get('Valute', {}):
                    rate = data['Valute'][currency]['Value']
                    history.append((date_str, rate))
            except:
                pass

        self.clear_screen()
        print("=" * 30)
        print(f"      ИСТОРИЯ {currency} ЗА {days} ДНЕЙ")
        print("=" * 30)

        if not history:
            print(f"\nНе удалось получить данные для {currency}")
            self.wait_for_enter()
            return

        print(f"\nПолучено данных за {len(history)} дней:")
        print("-" * 30)

        for date_str, rate in sorted(history):
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'][date_obj.weekday()]

            if date_obj.weekday() >= 5:
                weekday = weekday + " (вых)"

            print(f"{date_str} ({weekday}): {rate:.4f} руб.")

        rates = [rate for _, rate in history]
        if rates:
            print("-" * 30)
            print(f"Статистика:")
            print(f"Средний курс: {sum(rates)/len(rates):.4f} руб.")
            print(f"Минимальный:  {min(rates):.4f} руб.")
            print(f"Максимальный: {max(rates):.4f} руб.")

        print("\n" + "=" * 50)
        self.wait_for_enter()

    def run(self):
        print("Запуск конвертера валют")

        while True:
            try:
                self.show_menu()
                choice = self.get_choice()

                if choice == 1:
                    self.knopka1_show_rates()
                elif choice == 2:
                    self.knopka2_convert()
                elif choice == 3:
                    self.knopka3_history()
                elif choice == 4:
                    break

            except KeyboardInterrupt:
                print("\n\nПрограмма завершена")
                break
            except Exception as e:
                print(f"\nЧто то пошло не так: {e}")
                self.wait_for_enter()

if __name__ == "__main__":
    app = ConverterValut()
    app.run()
