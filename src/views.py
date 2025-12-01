import json
from datetime import datetime

from .services import get_currency_rates, get_stock_prices
from .utils import (calculate_cards_statistics, filter_transactions_by_date, get_greeting, get_top_transactions,
                    logger, read_transactions_excel)


def main_page(target_date: str) -> dict:
    """Главная функция, возвращающая JSON-ответ для веб-страницы"""
    with open("user_settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
    logger.info("Настройки пользователя загружены")

    df = read_transactions_excel("data/operations.xlsx")
    logger.info(f"Загружено {len(df)} транзакций")

    filtered_df = filter_transactions_by_date(df, target_date)
    logger.info(f"Отфильтровано {len(filtered_df)} транзакций за период")

    result = {
        "greeting": get_greeting(datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")),
        "cards": calculate_cards_statistics(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }
    logger.info("Главная страница сформирована успешно")
    return result


if __name__ == "__main__":
    # Тестируем на примере даты
    test_date = "2021-12-20 14:30:00"
    result = main_page(test_date)
    print(json.dumps(result, indent=2, ensure_ascii=False))
