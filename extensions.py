import json
import requests
from conf import keys


class ConvertionExeption(Exception):
    pass


class CriptoConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption(f'Вы ввели одинаковые валюты {base}')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Неудалось обработать валюту {quote} ')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Неудалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total = json.loads(r.content)[keys[base]]
        new_price = total * amount

        return new_price
