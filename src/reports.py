import json
import functools
import pandas as pd
from datetime import datetime, timedelta
from typing import Callable, Any, Optional


def report_to_file(func: Callable) -> Callable:
    """Декоратор для записи результата в файл с автоименем"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Вызываем оригинальную функцию
        result = func(*args, **kwargs)

        # Автоматическое имя файла: report_имяфункции_датавремя.json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{func.__name__}_{timestamp}.json"

        # Записываем результат в файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        print(f"Отчет сохранен в файл: {filename}")
        return result

    return wrapper


def report_to_file_with_name(filename: str) -> Callable:
    """Декоратор для записи результата в указанный файл"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            # Используем переданное имя файла
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)

            print(f"Отчет сохранен в файл: {filename}")
            return result

        return wrapper

    return decorator


def get_last_three_months_period(date: Optional[str] = None) -> tuple[datetime, datetime]:
    """Возвращает период: начало 3 месяцев назад и конец (указанная дата)"""
    if date is None:
        target_date = datetime.now()
    else:
        target_date = datetime.strptime(date, "%Y-%m-%d")

    # Начало периода: 3 месяца назад от указанной даты
    start_date = target_date - timedelta(days=90)

    return start_date, target_date


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты по дням недели за последние 3 месяца"""

    # Получаем период анализа
    start_date, end_date = get_last_three_months_period(date)

    # Создаем копию данных
    df = transactions.copy()
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format="%d.%m.%Y %H:%M:%S")

    # Фильтруем по периоду и только расходы (отрицательные суммы)
    period_mask = (df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)
    expenses_mask = df['Сумма операции'] < 0

    filtered_df = df[period_mask & expenses_mask]

    if filtered_df.empty:
        return pd.DataFrame()

    # Добавляем день недели и считаем средние траты
    result = (
        filtered_df
        .assign(day_of_week=filtered_df['Дата операции'].dt.day_name())
        .groupby('day_of_week')['Сумма операции']
        .apply(lambda x: abs(x).mean())
        .round(2)
        .reset_index()
        .rename(columns={'Сумма операции': 'average_spent'})
    )

    return result


@report_to_file
def spending_by_weekday_auto(transactions: pd.DataFrame,
                            date: Optional[str] = None) -> pd.DataFrame:
    """с автоматическим именем файла отчета"""
    return spending_by_weekday(transactions, date)


@report_to_file_with_name("weekly_spending_report.json")
def spending_by_weekday_custom(transactions: pd.DataFrame,
                              date: Optional[str] = None) -> pd.DataFrame:
    """с указанным именем файла отчета"""
    return spending_by_weekday(transactions, date)