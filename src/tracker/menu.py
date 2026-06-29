import os
from datetime import datetime, timedelta

from tracker.stats import (
    calculate_streak,
    get_homework_stats,
    get_previous_week_stats,
    get_today_entry,
)
from tracker.storage import load_goal, load_journal, save_goal, save_journal


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_program():
    while True:
        clear_screen()
        all_days = load_journal()
        current_streak = calculate_streak(all_days)
        weekly_goal = load_goal()

        print("\n" + "=" * 40)
        print("         --- PYTHON JOURNEY ---")
        print(f"        🔥 ВАШ СТРАЙК: {current_streak} ДН. 🔥")
        print("=" * 40)
        print(f" 🎯 ЦЕЛЬ НА НЕДЕЛЮ: {weekly_goal}")
        print("=" * 40)
        print("1. Добавить учебу или отдых")
        print("2. Написать в дневник (Итоги дня перед сном)")
        print("3. Посмотреть всю статистику")
        print("4. Удалить запись (Выбор по номеру)")
        print("5. Посмотреть итоги за неделю (Последние 7 дней)")
        print("6. Выйти из программы")
        print("=" * 40)

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            clear_screen()
            print("--- ВЫБОР ДАТЫ ДЛЯ УЧЕБЫ/ОТДЫХА ---")
            print("1. Записать за СЕГОДНЯ")
            print("2. Записать за ВЧЕРА (Забытая запись)")
            print("0. Назад в главное меню")
            date_choice = input("\nВыберите вариант: ")

            if date_choice == "0":
                continue
            if date_choice == "1":
                target_date = datetime.now().strftime("%d.%m.%Y")
            elif date_choice == "2":
                target_date = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
            else:
                print("Ошибка: нужно выбрать 1, 2 или 0!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            clear_screen()
            print(f"--- ДОБАВЛЕНИЕ ДАННЫХ ЗА ДАТУ [{target_date}] ---")
            print("1. Я в этот день Учился")
            print("2. Я в этот день Отдыхал")
            print("0. Назад")
            status = input("\nВыберите действие: ")

            if status == "0":
                continue

            today_entry = get_today_entry(all_days, target_date)

            if status == "1":
                try:
                    minutes = int(input("Сколько минут занимались? "))
                except ValueError:
                    print("Ошибка: введите минуты цифрами!")
                    input("\nНажмите Enter, чтобы вернуться...")
                    continue
                topic = input("Какую тему изучали или повторяли? ")

                if today_entry:
                    print("\nЗа этот день уже есть запись. Объединяем данные...")
                    today_entry["status"] = "Учеба"
                    today_entry["minutes"] = today_entry.get("minutes", 0) + minutes
                    if today_entry.get("topic") in ["Ничего, отдыхал", "Не занимался"]:
                        today_entry["topic"] = topic
                    else:
                        today_entry["topic"] = (
                            str(today_entry.get("topic", "")) + " -> " + topic
                        )
                else:
                    day_data = {
                        "date": target_date,
                        "status": "Учеба",
                        "minutes": minutes,
                        "topic": topic,
                        "rating": 0,
                        "achievement": "Пока нет записи в дневнике",
                    }
                    all_days.append(day_data)

            elif status == "2":
                if today_entry and today_entry.get("status") == "Учеба":
                    print(
                        f"\nОшибка! За {target_date} уже есть запись об Учебе. Отдых добавить нельзя."
                    )
                    input("\nНажмите Enter, чтобы вернуться...")
                    continue
                if today_entry and today_entry.get("status") == "Отдых":
                    print(f"\nЗа {target_date} уже отмечен отдых!")
                    input("\nНажмите Enter, чтобы вернуться...")
                    continue

                if today_entry:
                    today_entry["status"] = "Отдых"
                    today_entry["minutes"] = 0
                    today_entry["topic"] = "Ничего, отдыхал"
                else:
                    day_data = {
                        "date": target_date,
                        "status": "Отдых",
                        "minutes": 0,
                        "topic": "Ничего, отдыхал",
                        "rating": 5,
                        "achievement": "Хорошо отдохнул и набрался сил",
                    }
                    all_days.append(day_data)

            save_journal(all_days)
            print("\nУспешно сохранено!")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        elif choice == "2":
            clear_screen()
            print("--- ЛИЧНЫЙ ДНЕВНИК ДОСТИЖЕНИЙ ---")
            print("1. Написать за СЕГОДНЯ")
            print("2. Написать за ВЧЕРА (Забытая запись)")
            print("0. Назад в главное меню")
            day_choice = input("\nВыберите вариант: ")

            if day_choice == "0":
                continue
            if day_choice == "1":
                target_date = datetime.now().strftime("%d.%m.%Y")
            elif day_choice == "2":
                target_date = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
            else:
                print("Ошибка: нужно выбрать 1, 2 или 0!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            clear_screen()
            print(f"--- ЗАПИСЬ В ДНЕВНИК ЗА ДАТУ [{target_date}] ---")
            print("Запишите ваши итоги дня.")
            try:
                rating = int(input("\nОцените продуктивность дня от 1 до 5: "))
            except ValueError:
                print("Ошибка: введите число от 1 до 5!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            achievement = input("Твое главное достижение за сегодня? ")
            today_entry = get_today_entry(all_days, target_date)

            if today_entry:
                today_entry["rating"] = rating
                if today_entry.get("achievement") == "Пока нет записи в дневнике":
                    today_entry["achievement"] = achievement
                else:
                    today_entry["achievement"] = (
                        str(today_entry.get("achievement", "")) + " | " + achievement
                    )
            else:
                day_data = {
                    "date": target_date,
                    "status": "Дневник",
                    "minutes": 0,
                    "topic": "Не занимался",
                    "rating": rating,
                    "achievement": achievement,
                }
                all_days.append(day_data)

            save_journal(all_days)
            print("\nЗапись в дневник успешно сохранена!")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        elif choice == "3":
            clear_screen()
            if not all_days:
                print("\nЖурнал пуст. Сначала добавьте хотя бы один день!")
                input("\nНажмите Enter, чтобы вернуться в меню...")
                continue

            total_minutes = 0
            study_days = 0
            rest_days = 0
            print("========== ИСТОРИЯ ОБУЧЕНИЯ ==========")
            for day in all_days:
                date = day["date"]
                status = day["status"]
                minutes = day.get("minutes", 0)
                topic = day.get("topic", "Нет данных")
                ach = day.get("achievement", "Нет записи")

                if status == "Учеба":
                    print(
                        f"[{date}] Учеба: {minutes} мин. Тема: {topic} | Победа: {ach}"
                    )
                    total_minutes += minutes
                    study_days += 1
                elif status == "Отдых":
                    print(f"[{date}] Отдых: Восстановление сил")
                    rest_days += 1
                elif status == "Дневник":
                    print(f"[{date}] Только Дневник: учебы не было | Победа: {ach}")

            total_hours = total_minutes / 60
            print("\n========== ОБЩИЕ ИТОГИ ==========")
            print("Всего учебных дней:", study_days)
            print("Всего дней отдыха:", rest_days)
            print("Общее время учебы в часах:", round(total_hours, 2))
            print("=================================")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        elif choice == "4":
            clear_screen()
            if len(all_days) == 0:
                print("\nЖурнал уже пуст, нечего удалять!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            print("========== ВЫБЕРИТЕ ЗАПИСЬ ДЛЯ УДАЛЕНИЯ ==========")
            for index, day in enumerate(all_days, start=1):
                print(
                    f"{index}. Дата: {day['date']} | Status: {day['status']} | Тема: {day.get('topic', 'Нет темы')}"
                )
            print("0. Отмена (Назад в меню)")
            print("==================================================")

            try:
                delete_choice = int(
                    input("\nВведите номер записи, которую хотите удалить: ")
                )
            except ValueError:
                print("Ошибка: нужно ввести число!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            if delete_choice == 0:
                continue
            if delete_choice < 1 or delete_choice > len(all_days):
                print("Ошибка: записи с таким номером нет!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            target_day = all_days[delete_choice - 1]
            print(
                f"\nВы выбрали запись за дату: {target_day['date']} ({target_day['status']})"
            )
            confirm = input(
                "Вы точно хотите её БЕЗВОЗВРАТНО удалить? (1 - Да, 0 - Нет): "
            )
            if confirm == "1":
                removed_day = all_days.pop(delete_choice - 1)
                save_journal(all_days)
                print(f"\nЗапись за дату {removed_day['date']} успешно удалена!")
            else:
                print("\nУдаление отменено.")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        elif choice == "5":
            clear_screen()
            if not all_days:
                print("\nЖурнал пуст. Сначала добавьте хотя бы один день!")
                input("\nНажмите Enter, чтобы вернуться в меню...")
                continue

            today = datetime.now()
            seven_days_ago = today - timedelta(days=7)
            week_minutes = 0
            week_study_days = 0
            week_topics = []
            week_achievements = []

            print(" ========== ИТОГИ ЗА ПОСЛЕДНИЕ 7 ДНЕЙ ==========")
            for day in all_days:
                try:
                    day_date = datetime.strptime(day["date"], "%d.%m.%Y")
                except ValueError:
                    continue

                if day_date >= seven_days_ago:
                    status = day["status"]
                    if status == "Учеба":
                        week_minutes += day.get("minutes", 0)
                        week_study_days += 1
                        week_topics.append(day.get("topic", ""))
                        rating_str = (
                            f" (Оценка: {day['rating']}/5)"
                            if day.get("rating", 0) > 0
                            else ""
                        )
                        print(
                            f"• [{day['date']}] {day.get('minutes', 0)} мин -> Тема: {day.get('topic', '')}{rating_str}"
                        )
                    elif status == "Отдых":
                        print(f"• [{day['date']}] Отдых")
                    elif status == "Дневник":
                        print(
                            f"• [{day['date']}] Только дневник (Оценка: {day.get('rating', 0)}/5)"
                        )

                    if (
                        "achievement" in day
                        and day["achievement"]
                        and day["achievement"] != "Пока нет записи в дневнике"
                    ):
                        week_achievements.append(
                            f"[{day['date']}] {day['achievement']}"
                        )

            print("\n СУММАРНО ЗА ЭТУ НЕДЕЛЮ:")
            print("Продуктивных дней:", week_study_days)
            print("Всего часов учебы:", round(week_minutes / 60, 1))
            if week_topics:
                print("Изученные темы:", ", ".join(filter(None, week_topics)))

            prev_week_stats = get_previous_week_stats(all_days)
            prev_minutes = prev_week_stats["minutes"]
            prev_study_days = prev_week_stats["study_days"]

            print("\n ========== СРАВНЕНИЕ С ПРОШЛОЙ НЕДЕЛЕЙ ==========")
            print(f"Прошлая неделя: {prev_study_days} дней, {round(prev_minutes / 60, 1)} часов")
            print(f"Эта неделя: {week_study_days} дней, {round(week_minutes / 60, 1)} часов")
            diff_days = week_study_days - prev_study_days
            diff_hours = round(week_minutes / 60, 1) - round(prev_minutes / 60, 1)
            diff_symbol = "+" if diff_hours >= 0 else ""
            print(f"Разница: {diff_symbol}{diff_days} дней, {diff_symbol}{diff_hours} часов")

            homework_stats = get_homework_stats(all_days)
            print("\n ========== СТАТИСТИКА ПО ДОМАШКАМ ==========")
            if homework_stats["homework_count"] > 0:
                print(f"Всего домашек: {homework_stats['homework_count']}")
                print(f"Общее время на домашки: {round(homework_stats['total_minutes'] / 60, 1)} часов")
                print(f"Среднее время на домашку: {homework_stats['avg_time']} минут")
            else:
                print("Домашек пока не было")

            if week_achievements:
                print("\n ВАШИ ДОСТИЖЕНИЯ ЗА НЕДЕЛЮ:")
                for ach in week_achievements:
                    print(f" {ach}")

            print("\n ПЛАНИРОВАНИЕ:")
            plan_choice = input(
                "Хотите записать/обновить цель на следующую неделю? (1 - Да, 0 - Назад в меню): "
            )
            if plan_choice == "1":
                next_goal = input(
                    "\nКакая твоя главная цель на следующую неделю курса? "
                )
                save_goal(next_goal)
                print(
                    f"Отлично! Цель '{next_goal}' принята. Зажжем на следующей неделе!"
                )
            else:
                print("\nХорошо, вернемся к этому позже!")
            print("==================================================")
            input("\nНажмите Enter, чтобы вернуться в меню...")

        elif choice == "6":
            clear_screen()
            print("До встречи! Удачи в обучении!")
            break
        else:
            print("Ошибка: такого пункта нет, выберите от 1 до 6.")
            input("\nНажмите Enter, чтобы попробовать снова...")
