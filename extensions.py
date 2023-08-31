
class ConversionError(Exception):
    pass


class FormatError(ConversionError):
    def __str__(self):
        return "Ошибка пользывателя \nНекорректное количество параметров. Введите команду в правильном формате."


class SameCurrencyError(ConversionError):
    def __str__(self):
        return "Ошибка пользывателя \nНевозможно перевести одинаковые валюты."


class InvalidCurrencyError(ConversionError):
    def __str__(self):
        return "Ошибка пользывателя \nНекорректное имя валюты."


class InvalidAmountError(ConversionError):
    def __str__(self):
        return "Ошибка пользывателя \nНевозможно обработать количество. Введите число."
