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


def f1(x): return x ** 3 - 3 * x ** 2 + 7 * x - 10


def f2(x): return math.sin(x)


def f3(x):
    if x == 0: raise ValueError("Деление на ноль!")
    return 1 / x


def f4(x): return math.sin(100 * x) * math.exp(-x ** 2)


def f5(x):
    res = 0.0
    for i in range(1, 101):
        res += math.sin(x * i) * math.cos(x / i)
    return res


def f6(x):
    if x <= 0: raise ValueError("Разрыв или выход за ОДЗ!")
    return 1 / math.sqrt(x)


def f7(x):
    if x >= 1: raise ValueError("Разрыв или выход за ОДЗ!")
    return 1 / math.sqrt(1 - x)


def f8(x):
    if x == 0: raise ValueError("Разрыв в нуле!")
    return 1 / math.sqrt(abs(x))


def f9(x):
    if x == 0: raise ValueError("Разрыв в нуле!")
    return 1 / (x ** 2)

def check_improper(func_id, a, b):

    singularities = {
        3: [(0, 1.0)],
        6: [(0, 0.5)],
        7: [(1, 0.5)],
        8: [(0, 0.5)],
        9: [(0, 2.0)]
    }

    if func_id not in singularities:
        return False, True, []

    sings_in_interval = []
    for point, p in singularities[func_id]:
        if a <= point <= b:
            sings_in_interval.append((point, p))

    if not sings_in_interval:
        return False, True, []

    converges = True
    for point, p in sings_in_interval:
        if p >= 1.0:
            converges = False
            break

    return True, converges, [pt for pt, p in sings_in_interval]


def exact_integral_variant1(a, b):
    def F(x): return (x ** 4) / 4.0 - (x ** 3) + 3.5 * x ** 2 - 10 * x

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


def compute_improper_wrapper(method, f, a, b, n, discontinuities):
    delta = 1e-5
    points = sorted([a] + [d for d in discontinuities if a <= d <= b] + [b])
    intervals = []

    def is_discontinuity(val):
        return any(abs(val - d) < 1e-9 for d in discontinuities)

    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]

        if abs(start - end) < 1e-9: continue

        if is_discontinuity(start): start += delta
        if is_discontinuity(end):   end -= delta

        if start < end:
            intervals.append((start, end))

    total_sum = 0.0
    for start, end in intervals:
        total_sum += compute_integral(method, f, start, end, n)

    return total_sum


def run_integration(method_name, method_shader, f, a, b, eps, k, discontinuities):
    table_width = 76
    separator = "=" * table_width
    thin_separator = "-" * table_width

    print(f"\n{separator}")
    print(f"{method_name.upper():^{table_width}}")
    print(separator)
    print(f" {'Шаг (n)':<12} | {'Интеграл':<14} | Погрешность")
    print(thin_separator)

    n = 4
    I0 = compute_improper_wrapper(method_shader, f, a, b, n, discontinuities)
    print(f" {n:<12} | {I0:<14.5f} |  -")

    while True:
        n *= 2
        if n > 16777216:
            print(separator)
            print(f"ОСТАНОВКА: Достигнут лимит итераций (n={n}).")
            return (method_name, I1, n, float('inf'))

        I1 = compute_improper_wrapper(method_shader, f, a, b, n, discontinuities)
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
    print("1. f(x) = -x^3 - x^2 - 2x + 1 (Вариант 10)")
    print("2. f(x) = sin(x)")
    print("3. f(x) = 1/x")
    print("4. f(x) = sin(100x) * exp(-x^2) (Осциллятор)")
    print("5. f(x) = Сумма(1..100) sin(x*i)*cos(x/i) (Убийца CPU)")
    print("--- Несобственные интегралы (Доп. задание) ---")
    print("6. f(x) = 1/sqrt(x)      (Сходится, разрыв в x=0 -> проверка точки a)")
    print("7. f(x) = 1/sqrt(1-x)    (Сходится, разрыв в x=1 -> проверка точки b)")
    print("8. f(x) = 1/sqrt(|x|)    (Сходится, разрыв в x=0 -> проверка внутри отрезка)")
    print("9. f(x) = 1/x^2          (Расходится, разрыв в x=0)")

    func_id = read_safe_int("\nВведите номер функции (1-9): ", 1, 9)
    funcs = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5, 6: f6, 7: f7, 8: f8, 9: f9}
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

    is_improper, converges, discontinuities = check_improper(func_id, a, b)

    print("\nЗапуск вычислений...\n")

    if is_improper:
        print("=" * 60)
        print("ВНИМАНИЕ: Обнаружен несобственный интеграл 2-го рода!")
        print(f"Точки бесконечного разрыва на отрезке: {discontinuities}")
        if not converges:
            print(">>> Интеграл не существует <<<")
            print("=" * 60)
            return
        else:
            print("Интеграл сходится. Продолжаем вычисления...")
            print("Применяется метод отступа (\u03B4 = 1e-5) от точек разрыва.")
        print("=" * 60)

    if func_id == 1:
        exact = exact_integral_variant1(a, b)
        print(f"Точное аналитическое значение (Ньютон-Лейбниц): {exact:.5f}\n")

    results_data = []
    start_time = time.perf_counter()

    results_data.append(
        run_integration("Левые прямоугольники", "left_rect", selected_f, a, b, eps, 1.0, discontinuities))
    results_data.append(
        run_integration("Правые прямоугольники", "right_rect", selected_f, a, b, eps, 1.0, discontinuities))
    results_data.append(
        run_integration("Средние прямоугольники", "mid_rect", selected_f, a, b, eps, 2.0, discontinuities))
    results_data.append(run_integration("Метод трапеций", "trapezoid", selected_f, a, b, eps, 2.0, discontinuities))
    results_data.append(run_integration("Метод Симпсона", "simpson", selected_f, a, b, eps, 4.0, discontinuities))

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