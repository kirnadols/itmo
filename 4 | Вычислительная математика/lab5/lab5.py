import numpy as np
import matplotlib.pyplot as plt
import math
import os


# ==========================================
# 0. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (ЗАЩИТА ОТ ДУРАКА)
# ==========================================
def get_float(prompt):
    """Безопасный ввод вещественного числа"""
    while True:
        try:
            return float(input(prompt).replace(',', '.'))
        except ValueError:
            print("[!] Ошибка: введите корректное число (например: 1.5 или -3).")


def get_int(prompt, min_val=None):
    """Безопасный ввод целого числа"""
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"[!] Ошибка: число должно быть не меньше {min_val}.")
                continue
            return val
        except ValueError:
            print("[!] Ошибка: введите целое число (например: 5).")


# ==========================================
# 1. ФОРМИРОВАНИЕ ТЕСТОВЫХ ДАННЫХ
# ==========================================
def create_test_files():
    """Создает 3 тестовых файла с наборами данных, если они не существуют."""
    files_data = {
        "test1_linear.txt": "1 2\n2 4\n3 6\n4 8\n5 10",
        "test2_var11.txt": "0.25 1.2557\n0.30 2.1764\n0.35 3.1218\n0.40 4.0482\n0.45 5.9875\n0.50 6.9195\n0.55 7.8359",
        "test3_uneven.txt": "0.15 1.25\n0.2 2.38\n0.33 3.79\n0.47 5.44"
    }
    for filename, content in files_data.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)


# ==========================================
# 2. МАТЕМАТИЧЕСКАЯ ЧАСТЬ (ТАБЛИЦЫ РАЗНОСТЕЙ)
# ==========================================
def divided_differences_table(x, y):
    """Строит таблицу разделенных разностей"""
    n = len(y)
    table = np.zeros((n, n))
    table[:, 0] = y
    for j in range(1, n):
        for i in range(n - j):
            # Защита от деления на ноль на всякий случай, хотя валидация ввода это исключает
            denom = x[i + j] - x[i]
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / denom if denom != 0 else 0
    return table


def finite_differences_table(y):
    """Строит таблицу конечных разностей"""
    n = len(y)
    table = np.zeros((n, n))
    table[:, 0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]
    return table


def print_diff_table(x, table, is_finite=False):
    """Красивый форматированный вывод таблицы"""
    name = "конечных" if is_finite else "разделенных"

    # Заголовок
    header = f"| {'X':^8} | {'Y':^9} |"
    for i in range(1, len(table)):
        header += f" {'d^' + str(i) + 'y':^9} |"

    border = "-" * len(header)

    print(f"\n{border}")
    print(f" Таблица {name} разностей ".center(len(border), '-'))
    print(border)
    print(header)
    print(border)

    # Строки
    for i in range(len(table)):
        row = f"| {x[i]:>8.4f} |"
        for j in range(len(table) - i):
            val = table[i][j]
            # Форматируем красивый вывод без -inf/inf, если вдруг проскочит
            if np.isinf(val) or np.isnan(val):
                row += f" {'-':>9} |"
            else:
                row += f" {val:>9.4f} |"
        print(row)
    print(border)


# ==========================================
# 3. МЕТОДЫ ИНТЕРПОЛЯЦИИ
# ==========================================
def lagrange_interpolation(x_data, y_data, x):
    n = len(x_data)
    result = 0.0
    for i in range(n):
        term = y_data[i]
        for j in range(n):
            if i != j:
                term *= (x - x_data[j]) / (x_data[i] - x_data[j])
        result += term
    return result


def newton_divided_interpolation(x_data, y_data, x):
    table = divided_differences_table(x_data, y_data)
    n = len(x_data)
    if abs(x - x_data[0]) <= abs(x - x_data[-1]):
        result = table[0][0]
        term = 1.0
        for i in range(1, n):
            term *= (x - x_data[i - 1])
            result += table[0][i] * term
        return result, "Ньютон (прямой ход)"
    else:
        result = table[-1][0]
        term = 1.0
        for i in range(1, n):
            term *= (x - x_data[n - i])
            result += table[n - i - 1][i] * term
        return result, "Ньютон (обратный ход)"


def gauss_interpolation(x_data, y_data, x):
    table = finite_differences_table(y_data)
    n = len(x_data)
    h = x_data[1] - x_data[0]
    idx = min(range(n), key=lambda i: abs(x_data[i] - x))
    t = (x - x_data[idx]) / h

    result = table[idx][0]
    term = 1.0
    fact = 1

    try:
        if x > x_data[idx]:
            for i in range(1, n):
                if i % 2 != 0:
                    term *= (t - i // 2)
                    idx_diff = idx - i // 2
                else:
                    term *= (t + i // 2)
                    idx_diff = idx - i // 2
                if idx_diff < 0 or idx_diff >= n - i: break
                fact *= i
                result += (term * table[idx_diff][i]) / fact
            return result, "Гаусс (1-я формула)"
        else:
            for i in range(1, n):
                if i % 2 != 0:
                    term *= (t + i // 2)
                    idx_diff = idx - (i // 2) - 1
                else:
                    term *= (t - i // 2)
                    idx_diff = idx - i // 2
                if idx_diff < 0 or idx_diff >= n - i: break
                fact *= i
                result += (term * table[idx_diff][i]) / fact
            return result, "Гаусс (2-я формула)"
    except IndexError:
        pass
    return result, "Гаусс (Остановлен по границе)"


def stirling_interpolation(x_data, y_data, x):
    res_g1, _ = gauss_interpolation(x_data, y_data, x + 1e-9)
    res_g2, _ = gauss_interpolation(x_data, y_data, x - 1e-9)
    return (res_g1 + res_g2) / 2, "Стирлинг (среднее Гаусса)"


def bessel_interpolation(x_data, y_data, x):
    table = finite_differences_table(y_data)
    h = x_data[1] - x_data[0]
    idx = min(range(len(x_data) - 1), key=lambda i: abs(x_data[i] + h / 2 - x))
    t = (x - x_data[idx]) / h

    result = (table[idx][0] + table[idx + 1][0]) / 2 + (t - 0.5) * table[idx][1]
    try:
        fact2 = 2
        term2 = t * (t - 1)
        result += term2 / fact2 * ((table[idx - 1][2] + table[idx][2]) / 2)
        fact3 = 6
        term3 = term2 * (t - 0.5)
        result += term3 / fact3 * table[idx - 1][3]
    except IndexError:
        pass
    return result, "Бессель"


# ==========================================
# 4. ИНТЕРФЕЙС И ВВОД ДАННЫХ
# ==========================================
def main():
    create_test_files()
    print("=== Лабораторная работа №5: Интерполяция ===")
    print("1. Ввод из файла (рекомендуется)")
    print("2. Ввод с клавиатуры")
    print("3. На основе функции")

    while True:
        choice = input("Выберите способ ввода (1/2/3): ")
        if choice in ['1', '2', '3']:
            break
        print("[!] Ошибка: введите 1, 2 или 3.")

    x_data, y_data = [], []

    if choice == '1':
        print("\nДоступные файлы: test1_linear.txt, test2_var11.txt, test3_uneven.txt")
        while True:
            fname = input("Имя файла (или 'exit' для выхода): ")
            if fname.lower() == 'exit':
                print("Выход из программы.")
                return
            if not fname:
                fname = "test2_var11.txt"
                print(f"По умолчанию выбран файл: {fname}")
            try:
                data = np.loadtxt(fname)
                if data.shape[1] != 2:
                    print("[!] Ошибка: Файл должен содержать ровно 2 столбца (X и Y).")
                    continue

                # Защита от дурака: Проверка уникальности узлов X
                x_temp = data[:, 0]
                if len(np.unique(x_temp)) != len(x_temp):
                    print("[!] Ошибка: В файле есть дублирующиеся узлы (X). Все X должны быть уникальными!")
                    continue

                x_data, y_data = x_temp, data[:, 1]
                print("[+] Данные успешно загружены!")
                break
            except Exception as e:
                print(f"[!] Ошибка чтения файла: {e}. Попробуйте еще раз.")

    elif choice == '2':
        n = get_int("Введите количество точек (минимум 2): ", min_val=2)
        print("Введите координаты x и y через пробел (по одной паре на строку):")
        for i in range(n):
            while True:
                try:
                    row = input(f"Точка {i + 1}: ").replace(',', '.').split()
                    if len(row) != 2:
                        print("[!] Ошибка: нужно ввести ровно 2 числа.")
                        continue

                    x_val = float(row[0])
                    # Защита от дурака: Проверка на дубликат X
                    if x_val in x_data:
                        print(f"[!] Ошибка: координата X = {x_val} уже введена! Узлы X должны быть уникальными.")
                        continue

                    x_data.append(x_val)
                    y_data.append(float(row[1]))
                    break
                except ValueError:
                    print("[!] Ошибка: введены некорректные числа.")

        # Сортируем данные по X для корректной работы алгоритмов (Гаусс, конечные разности)
        sorted_indices = np.argsort(x_data)
        x_data = np.array(x_data)[sorted_indices]
        y_data = np.array(y_data)[sorted_indices]

    elif choice == '3':
        while True:
            f_choice = input("Выберите функцию: 1) sin(x)  2) sqrt(x) : ")
            if f_choice in ['1', '2']:
                break
            print("[!] Ошибка: введите 1 или 2.")

        func = math.sin if f_choice == '1' else math.sqrt
        a = get_float("Начало интервала a: ")

        while True:
            b = get_float("Конец интервала b: ")
            if b > a: break
            print("[!] Ошибка: конец интервала должен быть строго больше начала.")

        n = get_int("Количество точек (минимум 2): ", min_val=2)

        x_data = np.linspace(a, b, n)
        y_data = np.array([func(x) for x in x_data])

    # Проверка на равноотстоящие узлы
    diffs = np.diff(x_data)
    is_evenly_spaced = np.allclose(diffs, diffs[0], atol=1e-5)

    print("\n=================================")
    print("        ИСХОДНЫЕ ДАННЫЕ")
    print("=================================")
    for x, y in zip(x_data, y_data):
        print(f"X: {x:>8.4f} | Y: {y:>8.4f}")

    # Вывод таблиц
    print_diff_table(x_data, divided_differences_table(x_data, y_data), is_finite=False)
    if is_evenly_spaced:
        print_diff_table(x_data, finite_differences_table(y_data), is_finite=True)
    else:
        print(
            "\n[!] Узлы неравноотстоящие. Конечные разности (и методы Гаусса/Стирлинга) неприменимы в классическом виде.")

    # Ввод точки интерполяции
    target_x = get_float("\nВведите значение X для интерполяции: ")

    print("\n=================================")
    print("      РЕЗУЛЬТАТЫ ИНТЕРПОЛЯЦИИ")
    print("=================================")

    y_lagrange = lagrange_interpolation(x_data, y_data, target_x)
    print(f"Многочлен Лагранжа: \t\t{y_lagrange:.6f}")

    y_newton, n_name = newton_divided_interpolation(x_data, y_data, target_x)
    print(f"Многочлен Ньютона: \t\t{y_newton:.6f} ({n_name})")

    y_gauss = y_stirling = y_bessel = None
    if is_evenly_spaced:
        y_gauss, g_name = gauss_interpolation(x_data, y_data, target_x)
        print(f"Многочлен Гаусса: \t\t{y_gauss:.6f} ({g_name})")

        y_stirling, s_name = stirling_interpolation(x_data, y_data, target_x)
        print(f"Схема Стирлинга (доп.): \t{y_stirling:.6f}")

        y_bessel, b_name = bessel_interpolation(x_data, y_data, target_x)
        print(f"Схема Бесселя (доп.): \t\t{y_bessel:.6f}")

    # ==========================================
    # 5. ПОСТРОЕНИЕ РАЗДЕЛЬНЫХ ГРАФИКОВ
    # ==========================================
    margin = (max(x_data) - min(x_data)) * 0.1 if len(x_data) > 1 else 0.5
    x_plot = np.linspace(min(x_data) - margin, max(x_data) + margin, 500)

    y_plot_lagrange = [lagrange_interpolation(x_data, y_data, xi) for xi in x_plot]
    y_plot_newton = [newton_divided_interpolation(x_data, y_data, xi)[0] for xi in x_plot]

    num_plots = 3 if is_evenly_spaced else 2
    fig, axes = plt.subplots(1, num_plots, figsize=(6 * num_plots, 5))
    fig.suptitle("Интерполяция функции различными методами", fontsize=16, y=1.05)

    if num_plots == 1: axes = [axes]

    axes[0].plot(x_plot, y_plot_lagrange, color="blue", linewidth=2, label="P(x)")
    axes[0].scatter(x_data, y_data, color="red", zorder=5, s=40, label="Узлы")
    axes[0].scatter([target_x], [y_lagrange], color="purple", marker="X", s=100, zorder=6, label=f"X={target_x}")
    axes[0].set_title("Многочлен Лагранжа", fontsize=12)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    axes[0].legend()

    axes[1].plot(x_plot, y_plot_newton, color="orange", linewidth=2, label="P(x)")
    axes[1].scatter(x_data, y_data, color="red", zorder=5, s=40)
    axes[1].scatter([target_x], [y_newton], color="purple", marker="X", s=100, zorder=6)
    axes[1].set_title(f"Многочлен Ньютона\n({n_name})", fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.6)
    axes[1].legend()

    if is_evenly_spaced:
        y_plot_gauss = [gauss_interpolation(x_data, y_data, xi)[0] for xi in x_plot]
        axes[2].plot(x_plot, y_plot_gauss, color="green", linewidth=2, label="P(x)")
        axes[2].scatter(x_data, y_data, color="red", zorder=5, s=40)
        axes[2].scatter([target_x], [y_gauss], color="purple", marker="X", s=100, zorder=6)
        axes[2].set_title(f"Многочлен Гаусса\n({g_name})", fontsize=12)
        axes[2].grid(True, linestyle='--', alpha=0.6)
        axes[2].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()