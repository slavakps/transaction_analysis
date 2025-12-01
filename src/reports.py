import functools
import json
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

from src.utils import logger


def report_to_file(func: Callable) -> Callable:
    """Декоратор для записи результата в файл с автоименем"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"Запуск отчета: {func.__name__}")

        # Вызываем оригинальную функцию
        result = func(*args, **kwargs)

        # Автоматическое имя файла: report_имяфункции_датавремя.json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{func.__name__}_{timestamp}.json"

        # Записываем результат в файл
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Отчет сохранен в файл: {filename}")
        return result

    return wrapper


def report_to_file_with_name(filename: str) -> Callable:
    """Декоратор для записи результата в указанный файл"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.info(f"Запуск отчета: {func.__name__} с именем файла: {filename}")

            result = func(*args, **kwargs)

            # Используем переданное имя файла
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)

            logger.info(f"Отчет сохранен в файл: {filename}")
            return result

        return wrapper

    return decorator


def get_last_three_months_period(date: Optional[str] = None) -> tuple[datetime, datetime]:
    """Возвращает период: начало 3 месяцев назад и конец (указанная дата)"""
    logger.info(f"Определение периода для даты: {date}")

    if date is None:
        target_date = datetime.now()
        logger.info("Дата не указана, используется текущая дата")
    else:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
            logger.info(f"Дата распознана в формате YYYY-MM-DD: {target_date}")
        except ValueError:
            target_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            logger.info(f"Дата распознана в формате YYYY-MM-DD HH:MM:SS: {target_date}")

    # Начало периода: 3 месяца назад от указанной даты
    start_date = target_date - timedelta(days=90)
    logger.info(f"Период анализа: с {start_date.date()} по {target_date.date()}")

    return start_date, target_date


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты по дням недели за последние 3 месяца"""
    logger.info(f"Анализ трат по дням недели для даты: {date}")

    # Получаем период анализа
    start_date, end_date = get_last_three_months_period(date)

    # Создаем копию данных
    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    logger.info("Даты операций преобразованы в datetime")

    # Фильтруем по периоду и только расходы (отрицательные суммы)
    period_mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
    expenses_mask = df["Сумма операции"] < 0

    filtered_df = df[period_mask & expenses_mask]
    logger.info(f"Отфильтровано {len(filtered_df)} транзакций-расходов за период")

    if filtered_df.empty:
        logger.warning("Нет данных о расходах за указанный период")
        return pd.DataFrame()

    # Добавляем день недели и считаем средние траты
    result = (
        filtered_df.assign(day_of_week=filtered_df["Дата операции"].dt.day_name())
        .groupby("day_of_week")["Сумма операции"]
        .apply(lambda x: abs(x).mean())
        .round(2)
        .reset_index()
        .rename(columns={"Сумма операции": "average_spent"})
    )

    logger.info(f"Найдены траты для {len(result)} дней недели")
    logger.debug(f"Результат анализа: {result.to_dict('records')}")

    return result


@report_to_file
def spending_by_weekday_auto(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Версия с автоматическим именем файла отчета"""
    logger.info("Запуск функции spending_by_weekday_auto")
    return spending_by_weekday(transactions, date)


# Для демонстрации декоратора с параметром (по заданию)
@report_to_file_with_name("weekly_spending_report.json")
def spending_by_weekday_custom(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Версия с указанным именем файла отчета"""
    logger.info("Запуск функции spending_by_weekday_custom")
    return spending_by_weekday(transactions, date)
