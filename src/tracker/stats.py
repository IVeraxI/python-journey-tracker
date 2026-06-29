"""Модуль для расчета учебной статистики и страйков."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set


def calculate_streak(all_days: List[Dict[str, Any]]) -> int:
    """Считает текущий страйк (серию) дней непрерывной учебы.

    Args:
        all_days: Список всех дней из журнала.

    Returns:
        Количество дней непрерывной учебы подряд.
    """
    if not all_days:
        return 0
    study_dates: Set[Any] = set()
    for day in all_days:
        if day.get("status") == "Учеба":
            try:
                dt = datetime.strptime(day["date"], "%d.%m.%Y").date()
                study_dates.add(dt)
            except ValueError:
                continue
    if not study_dates:
        return 0
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    if today not in study_dates and yesterday not in study_dates:
        return 0
    current_check = today if today in study_dates else yesterday
    streak = 0
    while current_check in study_dates:
        streak += 1
        current_check -= timedelta(days=1)
    return streak


def get_today_entry(
    all_days: List[Dict[str, Any]], current_date: str
) -> Optional[Dict[str, Any]]:
    """Ищет запись в журнале за конкретную дату.

    Args:
        all_days: Список всех дней из журнала.
        current_date: Строка с датой в формате ДД.ММ.ГГГГ.

    Returns:
        Словарь с данными за день или None, если запись не найдена.
    """
    for day in all_days:
        if day["date"] == current_date:
            return day
    return None


def get_previous_week_stats(all_days: List[Dict[str, Any]]) -> Dict[str, int]:
    """Считает статистику за прошлую неделю (дни 8-14 дней назад).

    Args:
        all_days: Список всех дней из журнала.

    Returns:
        Словарь с ключами 'minutes' и 'study_days'.
    """
    today = datetime.now()
    prev_week_start = today - timedelta(days=14)
    prev_week_end = today - timedelta(days=8)

    prev_minutes = 0
    prev_study_days = 0

    for day in all_days:
        try:
            day_date = datetime.strptime(day["date"], "%d.%m.%Y")
        except ValueError:
            continue

        if prev_week_start <= day_date <= prev_week_end:
            if day.get("status") == "Учеба":
                prev_minutes += day.get("minutes", 0)
                prev_study_days += 1

    return {"minutes": prev_minutes, "study_days": prev_study_days}


def get_homework_stats(all_days: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Считает статистику по домашкам за всё время.

    Args:
        all_days: Список всех дней из журнала.

    Returns:
        Словарь с ключами 'total_minutes', 'homework_count', 'avg_time'.
    """
    homework_minutes = 0
    homework_count = 0

    for day in all_days:
        topic = day.get("topic", "").lower()
        if "домашка" in topic and day.get("status") == "Учеба":
            homework_minutes += day.get("minutes", 0)
            homework_count += 1

    avg_time = homework_minutes / homework_count if homework_count > 0 else 0

    return {
        "total_minutes": homework_minutes,
        "homework_count": homework_count,
        "avg_time": round(avg_time, 1)
    }
