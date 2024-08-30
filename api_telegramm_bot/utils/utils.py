from typing import BinaryIO, Optional


def is_number(text: str) -> Optional[int]:
    """
    Функция преобразует строку в целое число
    :param text: Строка
    :return: выводит целое число или None если строку нельзя преобразовать в целое число
    """
    try:
        return int(text)
    except (ValueError, TypeError):
        pass


def is_float(text: str) -> Optional[float]:
    """
    Функция преобразует строку в вещественное число
    :param text: Строка
    :return: выводит вещественное число или None если строку нельзя преобразовать в вещественное число
    """
    try:
        return float(text)
    except (ValueError, TypeError):
        pass



