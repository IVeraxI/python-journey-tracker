import json
from datetime import datetime

while True:
    print("\n--- PYTHON JOURNEY ---")
    print("1. Добавить новый день (учеба или отдых)")
    print("2. Посмотреть всю статистику")
    print("3. Удалить последнюю запись")
    print("4. Выйти из программы")

    choice = input("Выберите пункт меню: ")

    if choice == "1":
        current_date = datetime.now().strftime("%d.%m.%Y")
        print("Запись за дату:", current_date)

        status = input("Вы сегодня (1) Учились или (2) Отдыхали? ")

        if status != "1" and status != "2":
            print("Ошибка: нужно выбрать 1 или 2!")
            continue

        # Сначала загружаем все прошлые дни, чтобы проверить на дубликаты
        try:
            with open("journal.json", "r", encoding="utf-8") as file:
                all_days = json.load(file)
        except FileNotFoundError:
            all_days = []

        # Ищем, есть ли уже запись за сегодня (Защита от дубликатов)
        today_entry = None
        for day in all_days:
            if day["date"] == current_date:
                today_entry = day
                break

        # Если пользователь учился
        if status == "1":
            minutes = int(input("Сколько минут занимались? "))
            topic = input("Какую тему изучали или повторяли? ")

            if today_entry:
                # Если запись за сегодня уже есть — обновляем её
                print("За сегодня уже есть запись. Объединяем данные...")
                today_entry["status"] = "Учеба"  # Если раньше был отдых, меняем на учебу
                today_entry["minutes"] += minutes  # Прибавляем новые минуты к старым
                # Дописываем тему через запятую, чтобы не стереть старую
                today_entry["topic"] = today_entry["topic"] + ", " + topic
            else:
                # Если сегодня записей еще не было — создаем новую
                day_data = {
                    "date": current_date,
                    "status": "Учеба",
                    "minutes": minutes,
                    "topic": topic
                }
                all_days.append(day_data)

        # Если пользователь отдыхал
        elif status == "2":
            if today_entry:
                print("За сегодня уже есть запись! Отдых нельзя добавить поверх учебы.")
                continue
            else:
                print("Отдых — это тоже важно для мозга!")
                day_data = {
                    "date": current_date,
                    "status": "Отдых",
                    "minutes": 0,
                    "topic": "Ничего, отдыхал"
                }
                all_days.append(day_data)

        # Сохраняем обновленный список обратно в файл
        with open("journal.json", "w", encoding="utf-8") as file:
            json.dump(all_days, file, ensure_ascii=False, indent=4)

        print("Успешно сохранено!")

    elif choice == "2":
        try:
            with open("journal.json", "r", encoding="utf-8") as file:
                all_days = json.load(file)

            total_minutes = 0
            study_days = 0
            rest_days = 0

            print("\n========== ИСТОРИЯ ОБУЧЕНИЯ ==========")

            for day in all_days:
                date = day["date"]
                status = day["status"]
                minutes = day["minutes"]
                topic = day["topic"]

                if status == "Учеба":
                    print(f"[{date}] {status}: занимался {minutes} мин. Тема: {topic}")
                    total_minutes += minutes
                    study_days += 1
                elif status == "Отдых":
                    print(f"[{date}] {status}: восстанавливал силы ☕")
                    rest_days += 1

            total_hours = total_minutes / 60

            print("\n========== ОБЩИЕ ИТОГИ ==========")
            print("Всего учебных дней:", study_days)
            print("Всего дней отдыха:", rest_days)
            print("Общее время учебы в минутах:", total_minutes)
            print("Общее время учебы в часах:", round(total_hours, 2))
            print("=================================")

        except FileNotFoundError:
            print("\nЖурнал пуст. Сначала добавьте хотя бы один день!")

    elif choice == "3":
        try:
            with open("journal.json", "r", encoding="utf-8") as file:
                all_days = json.load(file)

            if len(all_days) == 0:
                print("\nЖурнал уже пуст, нечего удалять!")
            else:
                # Удаляем самый последний день из списка
                removed_day = all_days.pop()

                with open("journal.json", "w", encoding="utf-8") as file:
                    json.dump(all_days, file, ensure_ascii=False, indent=4)

                print(f"\nЗапись за дату {removed_day['date']} успешно удалена!")

        except FileNotFoundError:
            print("\nЖурнал пуст. Сначала добавьте хотя бы один день!")

    elif choice == "4":
        print("До встречи! Удачи в обучении!")
        break

    else:
        print("Ошибка: такого пункта нет, выберите от 1 до 4.")
