import pytest
import pandas as pd
from datetime import datetime, timedelta
from reports import get_last_three_months_period, spending_by_weekday


def test_get_last_three_months_period():
    """Тест функции определения периода"""
    # Тест с указанной датой
    start, end = get_last_three_months_period("2024-01-15")
    assert end == datetime(2024, 1, 15)
    assert start == datetime(2024, 1, 15) - timedelta(days=90)

    # Тест без даты (используется текущая дата)
    start, end = get_last_three_months_period()
    assert isinstance(start, datetime)
    assert isinstance(end, datetime)


def test_spending_by_weekday(sample_transactions):
    """Тест анализа трат по дням недели"""
    df = sample_transactions.copy()

    # Вызываем функцию с тестовой датой
    result = spending_by_weekday(df, "2021-12-31")

    # Проверяем структуру результата
    assert isinstance(result, pd.DataFrame)
    assert 'day_of_week' in result.columns
    assert 'average_spent' in result.columns

    # Проверяем что есть данные
    assert len(result) > 0

    # Проверяем что средние траты положительные числа
    assert all(result['average_spent'] > 0)