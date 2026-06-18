from structures import Stack, TreeNode

PRECEDENCE = {
    'u-': 3,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}

def infix_to_postfix(expression):

    expression = expression.replace(' ', '')

    if not expression:
        raise ValueError("Ошибка: выражение пустое")

    if expression[0] in '+-*/':
        if expression[0] != '-':
            raise ValueError(f"Ошибка: выражение не может начинаться с операции '{expression[0]}'")
    if expression[-1] in '+-*/':
        raise ValueError(f"Ошибка: выражение не может заканчиваться операцией '{expression[-1]}'")

    for i in range(len(expression)):
        char = expression[i]
        prev_char = expression[i - 1] if i > 0 else ''
        next_char = expression[i + 1] if i + 1 < len(expression) else ''

        if char in '+-*/':
            is_unary_minus = (
                char == '-'
                and (i == 0 or prev_char == '(' or prev_char in '+-*/')
            )

            if not is_unary_minus:
                if prev_char not in ')' and not prev_char.isalnum():
                    raise ValueError(
                        f"Операция '{char}' на позиции {i + 1} "
                        "не имеет левого операнда"
                    )
                if next_char not in '(-' and not next_char.isalnum():
                    raise ValueError(
                        f"Операция '{char}' на позиции {i + 1} "
                        "не имеет правого операнда"
                    )

    operator_stack = Stack()

    output = []

    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isdigit() or char.isalpha():

            operand = char
            while i + 1 < len(expression) and expression[i + 1].isdigit():
                i += 1
                operand += expression[i]

            output.append(operand)

        elif char == '(':
            operator_stack.push(char)

        elif char == ')':
            while not operator_stack.is_empty() and operator_stack.peek() != '(':
                output.append(operator_stack.pop())

            if not operator_stack.is_empty() and operator_stack.peek() == '(':
                operator_stack.pop()
            else:
                raise ValueError("Ошибка: лишняя закрывающая скобка ')'")

        elif char in PRECEDENCE:

            if char == '-' and (
                i == 0
                or expression[i - 1] == '('
                or expression[i - 1] in PRECEDENCE
            ):
                operator_stack.push('u-')
            else:
                while (
                    not operator_stack.is_empty()
                    and operator_stack.peek() != '('
                    and PRECEDENCE.get(operator_stack.peek(), 0) >= PRECEDENCE[char]
                ):
                    output.append(operator_stack.pop())

                operator_stack.push(char)

        else:
            raise ValueError(f"Ошибка: неизвестный символ '{char}' в выражении")

        i += 1

    while not operator_stack.is_empty():
        top = operator_stack.pop()
        if top == '(' or top == ')':
            raise ValueError("Ошибка: непарные скобки в выражении")
        output.append(top)

    return output


def build_expression_tree(postfix_tokens):

    stack = Stack()

    for token in postfix_tokens:

        if token not in PRECEDENCE and token != 'u-':
            node = TreeNode(token)
            stack.push(node)

        elif token == 'u-':
            operand = stack.pop()
            if operand is None:
                raise ValueError("Ошибка: не хватает операнда для унарного минуса")

            node = TreeNode('u-', left=None, right=operand)
            stack.push(node)

        else:
            right = stack.pop()
            left = stack.pop()

            if right is None or left is None:
                raise ValueError(
                    f"Ошибка: не хватает операндов для операции '{token}'"
                )

            node = TreeNode(token, left=left, right=right)
            stack.push(node)

    if stack.size() != 1:
        raise ValueError("Ошибка: некорректное выражение (проверьте скобки)")

    return stack.pop()


def evaluate_tree(node, variables=None):

    if variables is None:
        variables = {}

    if node.is_leaf():
        value = node.value

        if value.isdigit():
            return int(value)

        if value in variables:
            return variables[value]

        raise ValueError(
            f"Ошибка: неизвестное значение переменной '{value}'. "
            f"Укажите значения всех переменных."
        )

    if node.value == 'u-':
        return -evaluate_tree(node.right, variables)

    left_value = evaluate_tree(node.left, variables)
    right_value = evaluate_tree(node.right, variables)

    if node.value == '+':
        return left_value + right_value
    if node.value == '-':
        return left_value - right_value
    if node.value == '*':
        return left_value * right_value
    if node.value == '/':
        if right_value == 0:
            raise ValueError("Ошибка: деление на ноль")
        return left_value / right_value

    raise ValueError(f"Ошибка: неизвестная операция '{node.value}'")


def simplify_tree(node):

    if node.is_leaf():
        return TreeNode(node.value)

    new_left = simplify_tree(node.left) if node.left else None
    new_right = simplify_tree(node.right) if node.right else None

    def is_number(n, target):
        return n.is_leaf() and n.value.isdigit() and int(n.value) == target

    def is_zero(n):
        return is_number(n, 0)

    def is_one(n):
        return is_number(n, 1)

    operation = node.value

    if operation == '+':
        if is_zero(new_left):
            return new_right
        if is_zero(new_right):
            return new_left

    if operation == '-':
        if is_zero(new_right):
            return new_left
        if is_zero(new_left):
            return TreeNode('u-', left=None, right=new_right)

    if operation == '*':
        if is_zero(new_left) or is_zero(new_right):
            return TreeNode('0')
        if is_one(new_left):
            return new_right
        if is_one(new_right):
            return new_left

    if operation == '/':
        if is_one(new_right):
            return new_left
        if is_zero(new_left):
            return TreeNode('0')

    return TreeNode(operation, left=new_left, right=new_right)


def tree_to_infix(node):

    if node.is_leaf():
        return str(node.value)

    if node.value == 'u-':
        return f"(-{tree_to_infix(node.right)})"

    left_str = tree_to_infix(node.left)
    right_str = tree_to_infix(node.right)

    return f"({left_str} {node.value} {right_str})"


def run_task20():

    print("\nЗадача 20: Дерево выражений")
    print("Введите выражение в инфиксной форме.")
    print("Операнды: целые числа и однобуквенные переменные.")
    print("Операции: +, -, *, /, скобки, унарный минус.")
    print("Пример: (a + b) * c")

    while True:
        user_input = input("Выражение: ").strip()

        if not user_input:
            print("Ошибка: выражение не может быть пустым. Попробуйте ещё раз.")
            continue

        if user_input == '0':
            print("Возврат в главное меню.")
            return

        try:
            postfix = infix_to_postfix(user_input)
            print(f"\nПостфиксная запись: {' '.join(postfix)}")

            tree = build_expression_tree(postfix)
            print(f"Дерево выражения: {tree}")

            while True:
                variables_input = input(
                    "\nВведите значения переменных через запятую "
                    "(например, a=2,b=3), или оставьте пустым, "
                    "чтобы пропустить вычисление: "
                ).strip()

                if not variables_input:
                    print("Вычисление пропущено: не указаны значения переменных.")
                    break

                if variables_input == '0':
                    print("Вычисление пропущено.")
                    break

                try:
                    variables = {}
                    for pair in variables_input.split(','):
                        name, value = pair.split('=')
                        variables[name.strip()] = float(value.strip())

                    result = evaluate_tree(tree, variables)
                    print(f"Результат вычисления: {result}")
                    break

                except ValueError as error:
                    print(f"Ошибка в значениях переменных: {error}")
                    print("Попробуйте ещё раз (или оставьте пустым/введите 0 для пропуска).")
                except ZeroDivisionError:
                    print("Ошибка: деление на ноль. Попробуйте другие значения переменных.")

            simplified = simplify_tree(tree)
            print(f"\nУпрощённое выражение: {tree_to_infix(simplified)}")
            print(f"Упрощённое дерево: {simplified}")

            break

        except ValueError as error:
            print(f"Ошибка: {error}")
            print("Попробуйте ввести выражение ещё раз (или введите 0 для выхода в меню).")
        except ZeroDivisionError:
            print("Ошибка: деление на ноль")
            print("Попробуйте ввести выражение ещё раз (или введите 0 для выхода в меню).")


if __name__ == "__main__":
    run_task20()