import pytest

from src.services import analyze_cashback_categories


def test_analyze_cashback_categories(sample_transactions):
    """Тест анализа выгодных категорий кешбэка"""
    df = sample_transactions.copy()

    result = analyze_cashback_categories(df, 2021, 12)

    assert isinstance(result, dict)
    assert len(result) == 3

    # Проверяем что категории отсортированы по убыванию кешбэка
    cashback_values = list(result.values())
    assert cashback_values == sorted(cashback_values, reverse=True)

    # Проверяем конкретные значения
    assert result["Электроника"] == 20.0
    assert result["Супермаркеты"] == 10.0
    assert result["Рестораны"] == 5.0


@pytest.mark.parametrize(
    "year,month,expected_categories",
    [
        (2021, 12, 3),  # Декабрь 2021 - 3 категории
        (2021, 11, 0),  # Ноябрь 2021 - нет данных (0 категорий)
        (2022, 1, 0),  # Январь 2022 - нет данных
    ],
)
def test_analyze_cashback_categories_different_months(sample_transactions, year, month, expected_categories):
    """Параметризованный тест для разных месяцев"""
    df = sample_transactions.copy()
    result = analyze_cashback_categories(df, year, month)
    assert len(result) == expected_categories


def test_analyze_cashback_categories_simple(sample_transactions):
    """Простой тест анализа кешбэка с использованием фикстуры"""
    df = sample_transactions.copy()

    result = analyze_cashback_categories(df, 2021, 12)

    # Проверяем результат
    expected = {"Электроника": 20.0, "Супермаркеты": 10.0, "Рестораны": 5.0}
    assert result == expected
