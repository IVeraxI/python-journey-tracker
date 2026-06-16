import os
import json
from datetime import datetime, timedelta

def clear_screen():
    """Полностью очищает экран консоли от старого текста"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_journal():
    try:
        with open("journal.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_journal(data):
    with open("journal.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def calculate_streak(all_days):
    if not all_days:
        return 0
    study_dates = set()
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

def get_today_entry(all_days, current_date):
    """Вспомогательная функция для поиска записи за сегодня"""
    for day in all_days:
        if day["date"] == current_date:
            return day
    return None


# Главный цикл программы
while True:
    clear_screen()
    all_days = load_journal()
    current_streak = calculate_streak(all_days)

    print("\n" + "=" * 30)
    print("      --- PYTHON JOURNEY ---")
    print(f"      🔥 ВАШ СТРАЙК: {current_streak} ДН. 🔥")
    print("=" * 30)
    print("1. Добавить учебу или отдых")
    print("2. Написать в дневник (Итоги дня перед сном)")
    print("3. Посмотреть всю статистику")
    print("4. Удалить запись (Выбор по номеру)")
    print("5. Посмотреть итоги за неделю (Последние 7 дней)")
    print("6. Выйти из программы")

    choice = input("Выберите пункт меню: ")

    if choice == "1":
        clear_screen()
        current_date = datetime.now().strftime("%d.%m.%Y")
        print(f"--- ДОБАВЛЕНИЕ УЧЕБЫ/ОТДЫХА [{current_date}] ---")
        print("1. Я сегодня Учился")
        print("2. Я сегодня Отдыхал")
        print("0. Назад в главное меню")

        status = input("\nВыберите действие: ")

        if status == "0":
            continue
        if status != "1" and status != "2":
            print("Ошибка: нужно выбрать 1, 2 или 0!")
            input("\nНажмите Enter, чтобы вернуться...")
            continue

        today_entry = get_today_entry(all_days, current_date)

        if status == "1":
            try:
                minutes = int(input("Сколько минут занимались? "))
            except ValueError:
                print("Ошибка: введите минуты цифрами!")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            topic = input("Какую тему изучали или повторяли? ")

            if today_entry:
                print("\nЗа сегодня уже есть запись. Объединяем данные...")
                today_entry["status"] = "Учеба"
                today_entry["minutes"] += minutes
                if today_entry["topic"] == "Ничего, отдыхал":
                    today_entry["topic"] = topic
                else:
                    today_entry["topic"] = today_entry["topic"] + ", " + topic
            else:
                day_data = {
                    "date": current_date,
                    "status": "Учеба",
                    "minutes": minutes,
                    "topic": topic,
                    "rating": 0,
                    "achievement": "Пока нет записи в дневнике"
                }
                all_days.append(day_data)

        elif status == "2":
            if today_entry and today_entry["status"] == "Учеба":
                print("\nОшибка! За сегодня уже есть запись об Учебе. Отдых нельзя добавить поверх учебы.")
                input("\nНажмите Enter, чтобы вернуться...")
                continue

            if today_entry:
                print("\nЗа сегодня уже отмечен отдых!")
            else:
                print("\nОтдых — это тоже важно для мозга!")
                day_data = {
                    "date": current_date,
                    "status": "Отдых",
                    "minutes": 0,
                    "topic": "Ничего, отдыхал",
                    "rating": 5,
                    "achievement": "Хорошо отдохнул и набрался сил"
                }
                all_days.append(day_data)

        save_journal(all_days)
        print("\nУспешно сохранено!")
        input("\nНажмите Enter, чтобы вернуться в меню...")

    elif choice == "2":
        clear_screen()
        current_date = datetime.now().strftime("%d.%m.%Y")
        print(f"--- ЛИЧНЫЙ ДНЕВНИК ДОСТИЖЕНИЙ [{current_date}] ---")
        print("Запишите ваши итоги дня перед сном.")
        print("0. Назад в главное меню")

        check_back = input("\nНажмите Enter для продолжения или 0 для отмены: ")
        if check_back == "0":
            continue

        try:
            rating = int(input("\nОцените продуктивность дня от 1 до 5: "))
        except ValueError:
            print("Ошибка: введите число от 1 до 5!")
            input("\nНажмите Enter, чтобы вернуться...")
            continue

        achievement = input("Твое главное достижение за сегодня? ")

        today_entry = get_today_entry(all_days, current_date)

        if today_entry:
            today_entry["rating"] = rating
            if today_entry["achievement"] == "Пока нет записи в дневнике":
                today_entry["achievement"] = achievement
            else:
                today_entry["achievement"] = today_entry["achievement"] + " | " + achievement
        else:
            day_data = {
                "date": current_date,
                "status": "Дневник",
                "minutes": 0,
                "topic": "Не занимался",
                "rating": rating,
                "achievement": achievement
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
            minutes = day["minutes"]
            topic = day["topic"]
            ach = day.get("achievement", "Нет записи")

            if status == "Учеба":
                print(f"[{date}] Учеба: {minutes} мин. Тема: {topic} | Победа: {ach}")
                total_minutes += minutes
                study_days += 1
            elif status == "Отдых":
                print(f"[{date}] Отдых: восстанавливал силы ☕")
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
            print(f"{index}. Дата: {day['date']} | Status: {day['status']} | Тема: {day['topic']}")
        print("0. Отмена (Назад в меню)")
        print("==================================================")

        try:
            delete_choice = int(input("\nВведите номер записи, которую хотите удалить: "))
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

        print(f"\nВы выбрали запись за дату: {target_day['date']} ({target_day['status']})")
        confirm = input("Вы точно хотите её БЕЗВОЗВРАТНО удалить? (1 - Да, 0 - Нет): ")

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

        print("📅 ========== ИТОГИ ЗА ПОСЛЕДНИЕ 7 ДНЕЙ ==========")

        for day in all_days:
            try:
                day_date = datetime.strptime(day["date"], "%d.%m.%Y")
            except ValueError:
                continue

            if day_date >= seven_days_ago:
                if day["status"] == "Учеба":
                    week_minutes += day["minutes"]
                    week_study_days += 1
                    week_topics.append(day["topic"])

                    rating_str = f" (Оценка: {day['rating']}/5)" if day.get('rating', 0) > 0 else ""
                    print(f"• [{day['date']}] {day['minutes']} мин -> Тема: {day['topic']}{rating_str}")
                elif day["status"] == "Отдых":
                    print(f"• [{day['date']}] Отдых ☕")
                elif day["status"] == "Дневник":
                    print(f"• [{day['date']}] Только дневник (Оценка: {day['rating']}/5)")

                if "achievement" in day and day["achievement"] and day["achievement"] != "Пока нет записи в дневнике":
                    week_achievements.append(f"[{day['date']}] {day['achievement']}")

        print("\n📈 СУММАРНО ЗА НЕДЕЛЮ:")
        print("Продуктивных дней:", week_study_days)
        print("Всего часов учебы:", round(week_minutes / 60, 1))

        if week_topics:
            print("Изученные темы:", ", ".join(week_topics))

        if week_achievements:
            print("\n🏆 ВАШИ ДОСТИЖЕНИЯ ЗА НЕДЕЛЮ:")
            for ach in week_achievements:
                print(f"  {ach}")

        print("\n🎯 ПЛАНИРОВАНИЕ:")
        plan_choice = input("Хотите записать цель на следующую неделю? (1 - Да, 0 - Назад в меню): ")

        if plan_choice == "1":
            next_goal = input("\nКакая твоя главная цель на следующую неделю курса? ")
            print(f"Отлично! Цель '{next_goal}' принята. Зажжем на следующей неделе!")
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
