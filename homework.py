import datetime as dt
import sys
date_format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        result = sum(element.amount for element in self.records
                     if element.date == dt.datetime.now().date())
        return result

    def get_week_stats(self):
        today_date = dt.datetime.now().date()
        total_amount = 0
        date_week_ago = today_date - dt.timedelta(days=6)
        for element in self.records:
            if date_week_ago <= element.date <= today_date:
                total_amount += element.amount
        return total_amount


class CashCalculator(Calculator):
    USD_RATE = float(70)
    EURO_RATE = float(85)

    def get_today_cash_remained(self, currency):
        total_amount = self.get_today_stats()
        currency_rates = {'usd': [CashCalculator.USD_RATE, 'USD'],
                          'eur': [CashCalculator.EURO_RATE, 'Euro'],
                          'rub': [float(1), 'руб']}
        if currency not in currency_rates:
            sys.exit('Валюта не найдена')
        currency_rate, currency_name = currency_rates[currency]
        cash_remained = abs(self.limit - total_amount) / currency_rate
        cash_to_string = '{0:.2f} {1}'.format(cash_remained, currency_name)
        if self.limit - total_amount > 0:
            result = f'На сегодня осталось {cash_to_string}'
        elif self.limit - total_amount == 0:
            result = 'Денег нет, держись'
        elif self.limit - total_amount < 0:
            result = f'Денег нет, держись: твой долг - {cash_to_string}'
        return result


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        total_amount = self.get_today_stats()
        calories_remained = self.limit - total_amount
        if calories_remained > 0:
            result = (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                      f'калорийностью не более {calories_remained} кКал')
        else:
            result = 'Хватит есть!'
        return result


if __name__ == '__main__':
    cash_calculator = CashCalculator(100000)
    cash_calculator.add_record(Record(amount=3000, comment='SSD'))
    cash_calculator.add_record(Record(amount=10000, comment='Beats'))
    cash_calculator.add_record(Record(amount=100000, comment='MacBook'))
    cash_calculator.add_record(Record(amount=60000, comment='IPhone',
                                      date='13.10.2020'))
    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('eur'))
    print(cash_calculator.get_today_cash_remained('test'))
    print(cash_calculator.get_week_stats())

    calories_calculator = CaloriesCalculator(3000)
    calories_calculator.add_record(Record(amount=1000, comment='Meat'))
    calories_calculator.add_record(Record(amount=1000, comment='Coke'))
    calories_calculator.add_record(Record(amount=500, comment='Salad',
                                          date='13.10.2020'))
    print(calories_calculator.get_today_stats())
    print(calories_calculator.get_calories_remained())
    print(calories_calculator.get_week_stats())
