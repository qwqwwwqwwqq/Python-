from task4 import run_task4
from task20 import run_task20


def print_menu():
    print("\n" + "=" * 40)
    print("       ИНДИВИДУАЛЬНЫЙ ПРОЕКТ (ИКМ)")
    print("=" * 40)
    print("1 - Задача 4: генерация кода машины")
    print("2 - Задача 20: дерево выражений")
    print("0 - Выход")
    print("=" * 40)


def get_user_choice():
    while True:
        user_input = input("Выберите пункт меню: ").strip()

        if user_input in ('0', '1', '2'):
            return user_input

        print("Ошибка: введите число от 0 до 2.")


def main():
    while True:
        print_menu()
        choice = get_user_choice()

        if choice == '0':
            print("\nВыход из программы. До свидания!")
            break

        if choice == '1':
            run_task4()

        elif choice == '2':
            run_task20()

        input("\nНажмите Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    main()
