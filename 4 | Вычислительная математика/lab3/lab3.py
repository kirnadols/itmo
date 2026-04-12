import math
import time


def read_safe_int(prompt, min_val, max_val):
    while True:
        try:
            val_str = input(prompt).strip()
            val = int(val_str)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Ошибка: Число должно быть в диапазоне от {min_val} до {max_val}.")
        except ValueError:
            print("Ошибка: Введите корректное целое число.")


def read_safe_float(prompt):
    while True:
        try:
            val_str = input(prompt).strip().replace(',', '.')
            return float(val_str)
        except ValueError:
            print("Ошибка: Введите корректное число (например, 2.5 или 2,5).")


def f1(x):
    return -x ** 3 - x ** 2 - 2 * x + 1


def f2(x):
    return math.sin(x)


def f3(x):
    if x == 0:
        raise ValueError("Деление на ноль! Функция 1/x не определена в x=0.")
    return 1 / x


def f4(x):
    return math.sin(100 * x) * math.exp(-x ** 2)


def f5(x):
    res = 0.0
    for i in range(1, 101):
        res += math.sin(x * i) * math.cos(x / i)
    return res


def exact_integral_variant1(a, b):
    def F(x):
        return -(x ** 4) / 4.0 - (x ** 3) / 3.0 - x ** 2 + x

    return F(b) - F(a)


def compute_integral(method, f, a, b, n):
    h = (b - a) / n

    if method == "left_rect":
        return h * sum(f(a + i * h) for i in range(n))

    elif method == "right_rect":
        return h * sum(f(a + (i + 1) * h) for i in range(n))

    elif method == "mid_rect":
        return h * sum(f(a + (i + 0.5) * h) for i in range(n))

    elif method == "trapezoid":
        s = 0.5 * (f(a) + f(b)) + sum(f(a + i * h) for i in range(1, n))
        return h * s

    elif method == "simpson":
        sum_odd = sum(f(a + i * h) for i in range(1, n, 2))
        sum_even = sum(f(a + i * h) for i in range(2, n - 1, 2))
        return (h / 3.0) * (f(a) + 4 * sum_odd + 2 * sum_even + f(b))


def run_integration(method_name, method_shader, f, a, b, eps, k):
    table_width = 76
    separator = "=" * table_width
    thin_separator = "-" * table_width

    print(f"\n{separator}")
    print(f"{method_name.upper():^{table_width}}")
    print(separator)
    print(f" {'Шаг (n)':<12} | {'Интеграл':<14} | Погрешность")
    print(thin_separator)

    n = 4
    I0 = compute_integral(method_shader, f, a, b, n)
    print(f" {n:<12} | {I0:<14.5f} |  -")

    while True:
        n *= 2

        if n > 16777216:
            print(separator)
            print(f"ОСТАНОВКА: Достигнут лимит итераций (n={n}). Точность не достигнута.")
            return (method_name, I1, n, float('inf'))

        I1 = compute_integral(method_shader, f, a, b, n)
        error = abs(I1 - I0) / ((2 ** k) - 1)

        if n <= 1024 or n % 16384 == 0:
            print(f" {n:<12} | {I1:<14.5f} |  {error:.6e}")

        if error <= eps:
            print(separator)
            print(f"ИТОГ: Интеграл = {I1:.5f} | Шагов = {n} | Погрешность = {error:.6e}")
            return (method_name, I1, n, error)

        I0 = I1

def main():
    print("=== Лабораторная работа №3. Численное интегрирование ===")
    print("Доступные функции:")
    print("1. f(x) = -x^3 - x^2 - 2x + 1 (Вариант 1)")
    print("2. f(x) = sin(x)")
    print("3. f(x) = 1/x")
    print("4. f(x) = sin(100x) * exp(-x^2) (Осциллятор - Убийца Рунге)")
    print("5. f(x) = Сумма(1..100) sin(x*i)*cos(x/i) (Compute-Bound - Убийца CPU)")

    func_id = read_safe_int("\nВведите номер функции (1-5): ", 1, 5)

    funcs = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5}
    selected_f = funcs[func_id]

    a = read_safe_float("Введите предел a: ")
    b = read_safe_float("Введите предел b: ")

    while a >= b:
        print("Ошибка: Верхний предел (b) должен быть строго больше нижнего (a).")
        b = read_safe_float("Введите предел b заново: ")

    eps = read_safe_float("Введите точность (например, 0.001): ")
    while eps <= 0:
        print("Ошибка: Точность должна быть строго положительным числом.")
        eps = read_safe_float("Введите точность заново: ")

    print("\nЗапуск вычислений...\n")

    if func_id == 1:
        exact = exact_integral_variant1(a, b)
        print(f"Точное аналитическое значение (Ньютон-Лейбниц): {exact:.5f}\n")

    results_data = []

    start_time = time.perf_counter()

    results_data.append(run_integration("Левые прямоугольники", "left_rect", selected_f, a, b, eps, 1.0))
    results_data.append(run_integration("Правые прямоугольники", "right_rect", selected_f, a, b, eps, 1.0))
    results_data.append(run_integration("Средние прямоугольники", "mid_rect", selected_f, a, b, eps, 2.0))
    results_data.append(run_integration("Метод трапеций", "trapezoid", selected_f, a, b, eps, 2.0))
    results_data.append(run_integration("Метод Симпсона", "simpson", selected_f, a, b, eps, 4.0))

    end_time = time.perf_counter()
    total_time = end_time - start_time

    table_width = 78
    separator = "=" * table_width
    thin_separator = "-" * table_width

    print("\n")
    print(separator)
    print(f"{'СВОДНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ':^{table_width}}")
    print(separator)
    print(f"{'Метод':<26} | {'Интеграл':<10} | {'Шагов (n)':<10} | Погрешность")
    print(thin_separator)

    for res in results_data:
        name, val, n, err = res
        print(f"{name:<26} | {val:10.5f} | {n:10d} | {err:.6e}")

    print(separator)
    print(f"Общее время вычислений: {total_time:.4f} сек")
    print("\nВычисления успешно завершены.")


if __name__ == "__main__":
    main()
