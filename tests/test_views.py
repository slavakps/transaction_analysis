import pytest
from src.views import main_page


def test_main_page_integration(sample_transactions):
    """Интеграционный тест главной страницы"""
    result = main_page("2021-12-20 14:30:00")

    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result