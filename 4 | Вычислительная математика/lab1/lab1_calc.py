
import sys
import os


def calculate_matrix_norm(A):
    n = len(A)
    norm = 0
    for i in range(n):
        if A[i][i] == 0:
            return float('inf')
        row_sum = sum(abs(A[i][j]) for j in range(n) if i != j) / abs(A[i][i])
        if row_sum > norm:
            norm = row_sum
    return norm


def make_diagonally_dominant(A, b):
    n = len(A)
    new_A = [[0] * n for _ in range(n)]
    new_b = [0] * n
    used_rows = set()

    for i in range(n):
        row_found = False
        for r in range(n):
            if r in used_rows:
                continue

            diag_val = abs(A[r][i])
            sum_others = sum(abs(A[r][j]) for j in range(n) if j != i)

            if diag_val >= sum_others and A[r][i] != 0:
                new_A[i] = A[r][:]
                new_b[i] = b[r]
                used_rows.add(r)
                row_found = True
                break

        if not row_found:
            return A, b, False

    return new_A, new_b, True


def gauss_seidel_method(A, b, epsilon, max_iterations=1000):
    n = len(A)

    A, b, is_dominant = make_diagonally_dominant(A, b)

    if not is_dominant:
        print("\n[ВНИМАНИЕ] Невозможно достичь строгого диагонального преобладания.")
        print("Итерационный процесс может не сойтись!")
    else:
        print("\n[INFO] Матрица успешно приведена к диагональному преобладанию.")

    for i in range(n):
        if A[i][i] == 0:
            raise ZeroDivisionError(
                f"Критическая ошибка: Диагональный элемент A[{i + 1}][{i + 1}] равен нулю. Деление на ноль невозможно.")

    norm = calculate_matrix_norm(A)
    print(f"[INFO] Норма матрицы C: {norm:.4f}")
    if norm >= 1:
        print("[ВНИМАНИЕ] Норма матрицы >= 1. Достаточное условие сходимости не выполнено.")

    print("\n" + "-" * 40)
    print("ИТЕРАЦИОННЫЙ ПРОЦЕСС")
    print("-" * 40)

    x = [0.0] * n
    x_new = [0.0] * n
    iterations = 0
    errors = [0.0] * n

    formatted_start = ", ".join([f"{val:.4f}" for val in x])
    print(f"Итерация 0: x = [{formatted_start}]")

    for k in range(max_iterations):
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        errors = [abs(x_new[i] - x[i]) for i in range(n)]
        max_error = max(errors)
        iterations += 1

        formatted_x = ", ".join([f"{val:.4f}" for val in x_new])
        print(f"Итерация {iterations}: x = [{formatted_x}], max_error = {max_error:.6e}")

        if max_error <= epsilon:
            print("\n[INFO] Достигнута заданная точность!")
            break

        x = x_new.copy()

    if iterations == max_iterations:
        print(
            f"\n[ВНИМАНИЕ] Достигнуто максимальное количество итераций ({max_iterations}). Точность {epsilon} не достигнута.")

    return x_new, iterations, errors


def read_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise IOError(f"Ошибка при чтении файла: {e}")

    content = content.replace(',', '.')
    tokens = content.split()

    if not tokens:
        raise ValueError("Файл пуст.")

    n = int(tokens[0])
    epsilon = float(tokens[1])
    expected_matrix_elements = n * (n + 1)

    if len(tokens) == 2 + expected_matrix_elements:
        max_iter = 1000
        matrix_tokens = tokens[2:]
    elif len(tokens) == 3 + expected_matrix_elements:
        max_iter = int(tokens[2])
        matrix_tokens = tokens[3:]
    else:
        raise ValueError(f"Несоответствие данных. Ожидалось {expected_matrix_elements} коэффициентов.")

    A = []
    b = []
    for i in range(n):
        start_idx = i * (n + 1)
        end_idx = start_idx + n
        row = [float(val) for val in matrix_tokens[start_idx:end_idx]]
        b_val = float(matrix_tokens[end_idx])
        A.append(row)
        b.append(b_val)

    return n, epsilon, max_iter, A, b


def main():
    print("Решение СЛАУ методом Гаусса-Зейделя (Вариант 10)")

    try:
        mode = input("Ввести данные с клавиатуры (1) или из файла (2)? Введите 1 или 2: ").strip()

        if mode == '2':
            filename = input("Введите имя файла (например, 19_19.txt): ").strip()
            n, epsilon, max_iter, A, b = read_from_file(filename)
            print(f"\n[INFO] Файл '{filename}' успешно прочитан.")

        elif mode == '1':
            n = int(input("Введите размерность матрицы n (от 1 до 20): "))
            epsilon = float(input("Введите требуемую точность epsilon: ").replace(',', '.'))
            max_iter = 1000

            print(f"Введите коэффициенты матрицы A и вектор b построчно:")
            A = []
            b = []
            for i in range(n):
                row_input = input(f"Строка {i + 1}: ").replace(',', '.').strip().split()
                row = list(map(float, row_input))
                A.append(row[:-1])
                b.append(row[-1])
        else:
            sys.exit("Ошибка: Неверный режим.")

        x_ans, iters, errors = gauss_seidel_method(A, b, epsilon, max_iter)

        print("\n" + "=" * 30)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ ВЫЧИСЛЕНИЙ")
        print("=" * 30)
        print("Вектор неизвестных x:")
        for i in range(n):
            print(f"  x_{i + 1} = {x_ans[i]:.6f}")

        print(f"\nОбщее количество итераций: {iters}")
        print("\nВектор погрешностей |x_i^(k) - x_i^(k-1)| на последнем шаге:")
        for i in range(n):
            print(f"  e_{i + 1} = {errors[i]:.6e}")

    except Exception as e:
        print(f"\n[ОШИБКА ВЫПОЛНЕНИЯ] {e}")


if __name__ == "__main__":
    main()