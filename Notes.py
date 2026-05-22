import os

NOTES_FILE = "notes.txt"


def clear_console():
    """Очищает консоль."""
    os.system("cls" if os.name == "nt" else "clear")


def wait_and_clear():
    """Ожидает нажатия Enter и очищает консоль."""
    input("\nДля выхода в меню нажмите Enter...")
    clear_console()


def init_notes_file():
    """Создаёт файл для заметок, если он не существует."""
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write("")


def load_notes():
    """Загружает все заметки из файла."""
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def save_notes(lines):
    """Сохраняет заметки в файл."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


def show_notes():
    """Показывает все заметки с нумерацией."""
    lines = load_notes()

    if not lines:
        print("=" * 50)
        print("Заметки не найдены!")
        return

    print("=" * 50)
    for i, note in enumerate(lines, 1):
        print(f"{i}. {note.strip()}")


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
    """Добавляет новую заметку."""
    print("=" * 50)
    note = input("Введите заметку, которую хотите добавить: ")

    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(note + "\n")

    print("=" * 50)
    print("Заметка добавлена!")


def action_update_note():
    """Обновляет существующую заметку."""
    print("=" * 50)
    lines = load_notes()

    if not lines:
        print("Нет заметок для обновления!")
        return

    show_notes()
    choice = get_user_choice(len(lines))

    if not choice:
        return

    new_note = input("Введите новый текст заметки: ")
    lines[choice - 1] = new_note + "\n"
    save_notes(lines)

    print("=" * 50)
    print("Заметка обновлена!")


def action_delete_note():
    """Удаляет заметку из файла."""
    print("=" * 50)
    lines = load_notes()

    if not lines:
        print("Нет заметок для удаления!")
        return

    show_notes()
    choice = get_user_choice(len(lines))

    if not choice:
        return

    deleted_note = lines[choice - 1].strip()
    del lines[choice - 1]
    save_notes(lines)

    print("=" * 50)
    print(f"Заметка '{deleted_note}' удалена!")


def main():
    """Главный цикл программы."""
    clear_console()
    init_notes_file()

    menu_actions = {
        "1": action_add_note,
        "2": action_update_note,
        "3": action_delete_note,
        "4": show_notes,
    }

    while True:
        print("Менеджер заметок")
        print("=" * 50)
        print("0. Выйти")
        print("1. Добавить заметку")
        print("2. Обновить заметку")
        print("3. Удалить заметку")
        print("4. Посмотреть заметки")
        print("=" * 50)

        choice = input("Выберите вариант: ")

        if choice == "0":
            break

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор")

        wait_and_clear()


if __name__ == '__main__':
    main()