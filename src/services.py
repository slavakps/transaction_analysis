import pandas as pd
import requests
import os
from dotenv import load_dotenv


def get_currency_rates(currencies: list) -> list:
    """Получает курсы валют из Frankfurter API"""
    try:
        currencies_str = ",".join(currencies)

        # Запрашиваем курсы относительно EUR
        url = f"https://api.frankfurter.app/latest?base=EUR&symbols={currencies_str}"
        response = requests.get(url, timeout=10)
        data = response.json()

        currency_rates = []
        for currency in currencies:
            if currency in data['rates']:
                # Конвертируем: 1 RUB = 1 / EUR_to_currency
                rate = 1 / data['rates'][currency]
                currency_rates.append({
                    'currency': currency,
                    'rate': round(rate, 2)
                })

        return currency_rates

    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        return []

load_dotenv()

def get_stock_prices(stocks: list) -> list:
    """Получает цены акций из API Ninjas"""
    api_key = os.getenv('NINJA_API_KEY')

    stock_prices = []

    for stock in stocks:
        url = f"https://api.api-ninjas.com/v1/stockprice?ticker={stock}"
        headers = {'X-Api-Key': api_key}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'price' in data:
                stock_prices.append({
                    'stock': stock,
                    'price': round(float(data['price']), 2)
                })
        else:
            print(f"Ошибка для {stock}: {response.status_code}")

    return stock_prices


def filter_data_by_month(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Фильтрует транзакции по указанному году и месяцу"""

    df_copy = df.copy()
    df_copy['Дата операции'] = pd.to_datetime(df_copy['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    # Фильтруем по году и месяцу
    filtered = df_copy[(df_copy['Дата операции'].dt.year == year) & (df_copy['Дата операции'].dt.month == month)]

    return filtered


def analyze_cashback_categories(df: pd.DataFrame, year: int, month: int) -> dict:
    """Анализирует выгодность категорий для повышенного кешбэка"""
    # Фильтруем данные
    filtered_data = filter_data_by_month(df, year, month)
    # Группируем по категориям и считаем кешбэк
    cashback_by_category = (
        filtered_data
        .groupby('Категория')['Кэшбэк']
        .sum()
        .round(2)
        .to_dict()
    )

    sorted_cashback = dict(
        sorted(cashback_by_category.items(), key=lambda x: x[1], reverse=True)
    )

    return sorted_cashback

def calculate_cashback_by_category(df: pd.DataFrame) -> pd.Series:
    """Считает суммарный кешбэк по категориям"""

    cashback_series = (df.groupby('Категория')['Кэшбэк'].sum().round(2))

    return cashback_series


def sort_cashback_results(cashback_series: pd.Series) -> dict:
    """Сортирует результаты по убыванию кэшбэка и преобразует в словарь"""

    # Сортировка по убыванию кешбэка и преобразование в словарь
    sorted_cashback = (cashback_series.sort_values(ascending=False).to_dict())

    return sorted_cashback


def analyze_cashback_categories(df: pd.DataFrame, year: int, month: int) -> dict:
    """Анализирует выгодность категорий для повышенного кешбэка"""

    filtered_data = filter_data_by_month(df, year, month)
    cashback_series = calculate_cashback_by_category(filtered_data)
    result = sort_cashback_results(cashback_series)

    return result


