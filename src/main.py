from .reports import spending_by_weekday_auto
from .services import analyze_cashback_categories
from .utils import read_transactions_excel
from .views import main_page


def main():
    """Главная функция, демонстрирующая все возможности приложения"""
    print("Transaction Analysis App")

    # Читаем данные
    df = read_transactions_excel("data/operations.xlsx")
    print("Данные успешно загружены\n")

    # Сразу спрашиваем дату
    print("Введите дату для анализа:")
    year = input("   Год (например, 2021): ").strip()
    month = input("   Месяц (1-12): ").strip()

    target_date = f"{year}-{month}-15 14:30:00"  # Примерная дата в середине месяца

    print(f"Анализ за {month}/{year}")

    print("1. ГЛАВНАЯ СТРАНИЦА")
    main_result = main_page(target_date)
    print(f"   Приветствие: {main_result['greeting']}")

    # Детали по картам
    print("Карты в отчете:")
    for card in main_result["cards"]:
        print(f"     - ****{card['last_digits']}")

    # Детали по топ транзакциям
    print("Топ-5 транзакций:")
    for i, transaction in enumerate(main_result["top_transactions"][:5], 1):
        print(f"     {i}. {transaction['date']} - {transaction['category']}: {abs(transaction['amount'])} руб.")

    # Детали по валютам
    print("Курсы валют:")
    for currency in main_result["currency_rates"]:
        print(f"     - {currency['currency']}: {currency['rate']} руб.")

    # Детали по акциям
    print("Цены акций:")
    for stock in main_result["stock_prices"]:
        print(f"     - {stock['stock']}: ${stock['price']}")

    # 2. Сервисы - анализ кешбэка
    print(f"СЕРВИСЫ - Анализ кешбэка за {month}/{year}")
    cashback_result = analyze_cashback_categories(df, int(year), int(month), 3)

    if cashback_result:
        print(f"Топ-{len(cashback_result)} самых выгодных категорий:")
        for category, cashback_amount in cashback_result.items():
            print(f"{category}: {cashback_amount} руб. кешбэка")
    else:
        print("В этом месяце нет категорий с кешбэком")

    # 3. Отчеты - траты по дням недели
    print(f"ОТЧЕТЫ - Траты по дням недели за {month}/{year}")
    weekly_report = spending_by_weekday_auto(df, target_date)
    if not weekly_report.empty:
        print(f"Дней с данными: {len(weekly_report)}")
        for _, row in weekly_report.iterrows():
            print(f"{row['day_of_week']}: {row['average_spent']} руб.")
    else:
        print("Нет данных за выбранный период")

    print("Анализ завершен!")


if __name__ == "__main__":
    main()
