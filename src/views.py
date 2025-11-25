import json
from datetime import datetime
from .utils import (
    read_transactions_exel,
    filter_transactions_by_date,
    get_greeting,
    calculate_cards_statistics,
    get_top_transactions,
)
from .services import get_stock_prices, get_currency_rates

def main_page(target_date: str) -> dict:
    """Главная функция, возвращающая JSON-ответ для веб-страницы"""
    with open("user_settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    df = read_transactions_exel("data/operations.xlsx")
    filtered_df = filter_transactions_by_date(df, target_date)

    result = {
        "greeting": get_greeting(datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")),
        "cards": calculate_cards_statistics(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }
    return result

if __name__ == "__main__":
    # Тестируем на примере даты
    test_date = "2021-12-20 14:30:00"
    result = main_page(test_date)
    print(json.dumps(result, indent=2, ensure_ascii=False))