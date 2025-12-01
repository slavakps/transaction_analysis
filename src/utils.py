import logging
import sys
from datetime import datetime

import pandas as pd


def parse_date(data_string: str) -> datetime:
    """Преобразует строку даты из формата YYYY-MM-DD HH:MM:SS в datetime"""
    return datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S")


def read_transactions_excel(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл с транзакциями и возвращает DataFrame"""
    df = pd.read_excel(file_path)
    return df


def filter_transactions_by_date(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    """Фильтрует транзакции с начала месяца по указанную дату"""
    target_dt = datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S")
    start_of_month = target_dt.replace(day=1)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    mask = (df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= target_dt)
    filtered_df = df[mask]
    return filtered_df


def get_greeting(time_input: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    hour = time_input.hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def calculate_cards_statistics(df: pd.DataFrame) -> list:
    """Рассчитывает статистику по картам"""

    card_stats = []

    df_with_cards = df[df["Номер карты"].notna()]
    grouped = df_with_cards.groupby("Номер карты")

    for card_number, group in grouped:
        last_digits = card_number[-4:]

        expenses = group[group["Сумма операции"] < 0]["Сумма операции"]
        total_spent = abs(expenses.sum())

        cashback = group["Кэшбэк"].fillna(0).sum()

        card_stats.append(
            {"last_digits": last_digits, "total_spent": round(total_spent, 2), "cashback": round(cashback, 2)}
        )
    return card_stats


def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> list:
    """Возвращает топ-5 транзакций по сумме платежа"""

    expenses_df = df[df["Сумма платежа"] < 0].copy()
    top_df = expenses_df.nsmallest(top_n, "Сумма платежа")

    top_transactions = []
    for _, row in top_df.iterrows():
        top_transactions.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return top_transactions


def setup_logging():
    """Настройка логирования для всего проекта"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("transaction_analysis.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    return logging.getLogger(__name__)


logger = setup_logging()
