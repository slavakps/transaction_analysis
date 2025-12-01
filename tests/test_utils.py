from datetime import datetime

import pytest

from src.utils import calculate_cards_statistics, filter_transactions_by_date, get_greeting, parse_date


@pytest.mark.parametrize(
    "hour,expected", [(8, "Доброе утро"), (14, "Добрый день"), (19, "Добрый вечер"), (2, "Доброй ночи")]
)
def test_get_greeting(hour, expected):
    """Параметризованный тест приветствий"""
    test_time = datetime(2024, 1, 1, hour, 0, 0)
    assert get_greeting(test_time) == expected


def test_parse_date():
    """Тест парсинга даты"""
    date_str = "2024-01-15 14:30:00"
    result = parse_date(date_str)
    expected = datetime(2024, 1, 15, 14, 30, 0)
    assert result == expected


def test_filter_transactions_by_date(sample_transactions, sample_date):
    """Тест фильтрации транзакций по дате"""
    df = sample_transactions.copy()

    result = filter_transactions_by_date(df, sample_date)
    print("Все даты в данных:")
    print(df["Дата операции"])
    print("Начало месяца:", datetime(2021, 12, 1))
    print("Конец периода:", datetime(2021, 12, 20, 14, 30, 0))
    print("Результат фильтрации:")
    print(result[["Дата операции", "Номер карты"]])
    assert len(result) == 2


def test_calculate_cards_statistics(sample_transactions):
    """Тест расчета статистики по картам"""
    result = calculate_cards_statistics(sample_transactions)

    assert len(result) == 2  # Две уникальные карты
    assert result[0]["last_digits"] == "4556"
    assert result[1]["last_digits"] == "7197"
