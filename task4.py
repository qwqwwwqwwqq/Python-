from structures import Stack


OPERATION_TO_COMMAND = {
    '+': 'AD',
    '-': 'SB',
    '*': 'ML',
    '/': 'DV',
}


def generate_machine_code(postfix_expression):

    stack = Stack()

    instructions = []

    temp_counter = 1

    total_operations = sum(1 for char in postfix_expression if char in OPERATION_TO_COMMAND)
    processed_operations = 0


    for char in postfix_expression:

        if char == ' ':
            continue

        if char.isalpha():
            stack.push(char.upper())
            continue

        if char in OPERATION_TO_COMMAND:

            processed_operations += 1

            right_operand = stack.pop()
            left_operand = stack.pop()

            if right_operand is None or left_operand is None:
                raise ValueError(
                    "в постфиксном выражении не хватает операндов "
                    f"для операции '{char}'."
                )

            command = OPERATION_TO_COMMAND[char]

            instructions.append(f"LD {left_operand}")
            instructions.append(f"{command} {right_operand}")

            if processed_operations != total_operations:
                temp_variable = f"T{temp_counter}"
                temp_counter += 1
                instructions.append(f"ST {temp_variable}")
                stack.push(temp_variable)
            else:
                pass
            continue

        raise ValueError(
            f"Ошибка: неизвестный символ '{char}' в постфиксном выражении."
        )


    if stack.size() != 1 and stack.size() != 0:
        raise ValueError(
            "Ошибка: постфиксное выражение некорректно. "
            f"В стеке осталось {stack.size()} элемента(ов) вместо 1."
        )

    return instructions


def run_task4():

    print("\nЗадача 4: Генерация кода для вычислительной машины")
    print("Введите выражение в постфиксной форме.")
    print("Операнды - однобуквенные переменные (a-z), операции: +, -, *, /")
    print("Пример: ABC*+DE-/")


    while True:
        user_input = input("Выражение: ").strip()

        if not user_input:
            print("Ошибка: выражение не может быть пустым. Попробуйте ещё раз.")
            continue

        if user_input == '0':
            print("Возврат в главное меню.")
            return

        try:
            instructions = generate_machine_code(user_input)

            print("\nСгенерированные инструкции для вычислительной машины:")
            for line in instructions:
                print(line)
            break

        except ValueError as error:
            print(f"Ошибка: {error}")
            print("Попробуйте ввести выражение ещё раз (или введите 0 для выхода в меню).")

if __name__ == "__main__":
    run_task4()