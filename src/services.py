import os

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import logger

load_dotenv()


def get_currency_rates(currencies: list) -> list:
    """Получает курсы валют из Exchangerate-API"""
    try:
        API_KEY = os.getenv("EXCHANGERATE_API_KEY")

        if not API_KEY:
            print("API ключ не найден в .env файле")
            return []

        # Запрашиваем курсы относительно RUB
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/RUB"
        response = requests.get(url, timeout=10)
        data = response.json()

        currency_rates = []
        for currency in currencies:
            if currency in data["conversion_rates"]:
                rate = 1 / data["conversion_rates"][currency]
                currency_rates.append({"currency": currency, "rate": round(rate, 2)})
        logger.info(f"Курсы валют получены: {currency_rates}")
        return currency_rates

    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return []


def get_stock_prices(stocks: list) -> list:
    """Получает цены акций из API Ninjas"""
    api_key = os.getenv("NINJA_API_KEY")

    stock_prices = []

    for stock in stocks:
        url = f"https://api.api-ninjas.com/v1/stockprice?ticker={stock}"
        headers = {"X-Api-Key": api_key}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if "price" in data:
                stock_prices.append({"stock": stock, "price": round(float(data["price"]), 2)})
        else:
            print(f"Ошибка для {stock}: {response.status_code}")

    return stock_prices


def filter_data_by_month(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Фильтрует транзакции по указанному году и месяцу"""

    df_copy = df.copy()
    df_copy["Дата операции"] = pd.to_datetime(df_copy["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Фильтруем по году и месяцу
    filtered = df_copy[(df_copy["Дата операции"].dt.year == year) & (df_copy["Дата операции"].dt.month == month)]

    return filtered


def calculate_cashback_by_category(df: pd.DataFrame) -> pd.Series:
    """Считает суммарный кешбэк по категориям"""

    cashback_series = df.groupby("Категория")["Кэшбэк"].sum().round(2)

    return cashback_series


def sort_cashback_results(cashback_series: pd.Series) -> dict:
    """Сортирует результаты по убыванию кэшбэка и преобразует в словарь"""

    # Сортировка по убыванию кешбэка и преобразование в словарь
    sorted_cashback = cashback_series.sort_values(ascending=False).to_dict()

    return sorted_cashback


def analyze_cashback_categories(df: pd.DataFrame, year: int, month: int, top_n: int = 3) -> dict:
    """Анализирует самые выгодные категории по сумме кэшбэка"""
    filtered_data = filter_data_by_month(df, year, month)
    expenses_data = filtered_data[filtered_data["Сумма операции"] < 0]
    logger.info(f"Анализ кэшбэка за {month}/{year}, топ-{top_n}")

    # Группируем по категориям и считаем кешбэк
    category_cashback = expenses_data.groupby("Категория")["Кэшбэк"].sum().sort_values(ascending=False)

    # Фильтруем категории с нулевым кэшбэком
    category_cashback = category_cashback[category_cashback > 0]

    # Берем топ-N категорий
    top_categories = category_cashback.head(top_n)

    # Форматируем результат
    result = {}
    for category, cashback_amount in top_categories.items():
        result[category] = round(cashback_amount, 2)
        logger.info(f"Найдено {len(result)} выгодных категорий")

    return result
