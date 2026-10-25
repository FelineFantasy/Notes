#!/usr/bin/env python3

"""
Simple note manager with CRUD operations and search functionality.
"""

import json
import os

NOTES_FILE = os.environ.get("NOTES_FILE", "notes.txt")


def clear_console():
    """Очищает консоль."""
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_enter():
    """Ожидает нажатия Enter и очищает консоль."""
    input("\nДля выхода в меню нажмите Enter...")
    clear_console()


def init_notes_file():
    """Создаёт файл для заметок, если он не существует."""
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write("")


def load_notes():
    """Загружает все заметки из файла, игнорируя пустые строки."""
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            lines = [line for line in f.readlines() if line.strip()]
            return lines
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Ошибка чтения: {e}")
        return []


def save_notes(lines):
    """Сохраняет заметки в файл."""
    if lines is None:
        lines = []
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


def display_notes(lines, show_header=True):
    """Отображает список заметок с нумерацией."""
    if show_header:
        print("=" * 50)

    if not lines:
        print("Заметки не найдены!")
        return

    for i, note in enumerate(lines, 1):
        print(f"{i}. {note.strip()}")


def show_notes():
    """Показывает все заметки с нумерацией."""
    lines = load_notes()
    display_notes(lines, show_header=True)


def add_note(text):
    """Добавляет заметку и возвращает сохранённый текст."""
    text = text.strip()

    if not text:
        raise ValueError("Заметка не может быть пустой!")

    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    return text


def update_note(index, text):
    """Заменяет заметку по номеру и возвращает её предыдущий текст."""
    text = text.strip()

    if not text:
        raise ValueError("Заметка не может быть пустой!")

    lines = load_notes()

    if not 1 <= index <= len(lines):
        raise IndexError("Неверный номер заметки")

    previous = lines[index - 1].strip()
    lines[index - 1] = text + "\n"
    save_notes(lines)

    return previous


def delete_note(index):
    """Удаляет заметку по номеру и возвращает её текст."""
    lines = load_notes()

    if not 1 <= index <= len(lines):
        raise IndexError("Неверный номер заметки")

    deleted = lines.pop(index - 1).strip()
    save_notes(lines)

    return deleted


def search_notes(keyword):
    """Возвращает заметки, содержащие ключевое слово (без учёта регистра)."""
    keyword = keyword.strip().lower()

    if not keyword:
        raise ValueError("Ключевое слово не может быть пустым!")

    return [note for note in load_notes() if keyword in note.lower()]


def export_notes(path):
    """Сохраняет заметки в JSON-файл и возвращает их количество."""
    notes = [
        {"id": number, "text": note.strip()}
        for number, note in enumerate(load_notes(), 1)
    ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return len(notes)


def get_user_choice(max_choice):
    """Получает от пользователя номер выбора."""
    try:
        choice = int(input("Введите номер: "))
        if 1 <= choice <= max_choice:
            return choice
        print("Неверный номер")
    except ValueError:
        print("Введите число!")
    return None


def action_add_note():
    print("=" * 50)
    note = input("Введите заметку, которую хотите добавить: ").strip()

    try:
        add_note(note)
    except ValueError as e:
        print(e)
        return

    print("=" * 50)
    print("Заметка добавлена!")


def action_update_note():
    """Обновляет существующую заметку."""
    print("=" * 50)
    lines = load_notes()

    if not lines:
        print("Нет заметок для обновления!")
        return

    display_notes(lines, show_header=False)
    choice = get_user_choice(len(lines))

    if not choice:
        return

    new_note = input("Введите новый текст заметки: ")

    try:
        update_note(choice, new_note)
    except (ValueError, IndexError) as e:
        print(e)
        return

    print("=" * 50)
    print("Заметка обновлена!")


def action_delete_note():
    """Удаляет заметку из файла."""
    print("=" * 50)
    lines = load_notes()

    if not lines:
        print("Нет заметок для удаления!")
        return

    display_notes(lines, show_header=False)
    choice = get_user_choice(len(lines))

    if not choice:
        return

    try:
        deleted_note = delete_note(choice)
    except IndexError as e:
        print(e)
        return

    print("=" * 50)
    print(f"Заметка '{deleted_note}' удалена!")


def action_search_notes():
    """Поиск заметок по ключевому слову."""
    print("=" * 50)
    keyword = input("Введите ключевое слово для поиска: ")

    try:
        found = search_notes(keyword)
    except ValueError as e:
        print(e)
        return

    if found:
        print(f"\nНайдено {len(found)} заметок:")
        display_notes(found, show_header=False)
    else:
        print("Заметки не найдены!")


def action_export_notes():
    """Экспортирует заметки в JSON-файл."""
    print("=" * 50)
    path = input("Введите имя JSON-файла (по умолчанию notes.json): ").strip()
    path = path or "notes.json"

    try:
        count = export_notes(path)
    except OSError as e:
        print(f"Ошибка экспорта: {e}")
        return

    print("=" * 50)
    print(f"Экспортировано заметок: {count} -> {path}")


def main():
    """Главный цикл программы."""
    clear_console()
    init_notes_file()

    menu = {
        "1": ("Добавить заметку", action_add_note),
        "2": ("Обновить заметку", action_update_note),
        "3": ("Удалить заметку", action_delete_note),
        "4": ("Посмотреть заметки", show_notes),
        "5": ("Поиск заметок", action_search_notes),
        "6": ("Экспорт заметок в JSON", action_export_notes),
    }

    while True:
        print("=" * 50)
        print("МЕНЕДЖЕР ЗАМЕТОК".center(50))
        print("=" * 50)
        for key, (name, _) in menu.items():
            print(f"{key}. {name}")
        print("0. Выйти")
        print("=" * 50)

        choice = input("Выберите вариант: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        if choice in menu:
            _, action = menu[choice]
            action()
        else:
            print("Неверный выбор!")

        wait_for_enter()


if __name__ == '__main__':
    main()
