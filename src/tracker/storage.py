import json
import os

# Автоматически создаем папку data, если её вдруг нет
os.makedirs("data", exist_ok=True)


def load_journal():
    try:
        with open("data/journal.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_journal(data):
    with open("data/journal.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_goal():
    try:
        with open("data/goal.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("goal", "Пока не поставлена")
    except FileNotFoundError:
        return "Пока не поставлена"


def save_goal(goal_text):
    with open("data/goal.json", "w", encoding="utf-8") as file:
        json.dump({"goal": goal_text}, file, ensure_ascii=False, indent=4)
