import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
import os

warnings.filterwarnings("ignore")


def original_function(x):
    return (5 * x) / (x ** 4 + 7)


def linear_func(x, a, b): return a * x + b


def poly2_func(x, a0, a1, a2): return a0 + a1 * x + a2 * x ** 2


def poly3_func(x, a0, a1, a2, a3): return a0 + a1 * x + a2 * x ** 2 + a3 * x ** 3


def exp_func(x, a, b): return a * np.exp(b * x)


def log_func(x, a, b): return a * np.log(x) + b


def power_func(x, a, b): return a * (x ** b)


def parse_float(val_str):
    return float(val_str.replace(',', '.'))


def clean_and_sort_data(x_list, y_list):
    if len(x_list) < 3:
        print("\n[ОШИБКА] Слишком мало данных! Нужно минимум 3 точки для построения графиков.")
        return None, None

    x_arr = np.array(x_list)
    y_arr = np.array(y_list)

    unique_x, indices = np.unique(x_arr, return_index=True)
    if len(unique_x) < len(x_arr):
        duplicates = len(x_arr) - len(unique_x)
        print(
            f"\n[ВНИМАНИЕ] Найдено {duplicates} точек с одинаковыми X. Дубликаты удалены, т.к. функция не может иметь несколько значений Y для одного X.")

    x_arr = x_arr[indices]
    y_arr = y_arr[indices]

    sort_idx = np.argsort(x_arr)
    return x_arr[sort_idx], y_arr[sort_idx]


def read_data_from_file(filename="data.txt"):
    if not os.path.exists(filename):
        print(f"\n[ОШИБКА] Файл '{filename}' не найден!")
        return None, None

    x_list, y_list = [], []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#') or line.lower().startswith('x'):
                    continue

                parts = line.split()
                if len(parts) != 2:
                    print(f"[ПРЕДУПРЕЖДЕНИЕ] Строка {line_num} пропущена: ожидалось 2 числа, найдено {len(parts)}.")
                    continue

                try:
                    x = parse_float(parts[0])
                    y = parse_float(parts[1])
                    x_list.append(x)
                    y_list.append(y)
                except ValueError:
                    print(f"[ПРЕДУПРЕЖДЕНИЕ] Строка {line_num} пропущена: текст '{line}' нельзя преобразовать в числа.")
    except Exception as e:
        print(f"\n[ОШИБКА] Непредвиденная ошибка при чтении файла: {e}")
        return None, None

    if not x_list:
        print("\n[ОШИБКА] В файле не найдено ни одной корректной строчки с данными!")
        return None, None

    print(f"\nУспешно считано {len(x_list)} сырых точек из файла {filename}.")
    return clean_and_sort_data(x_list, y_list)


def read_data_from_console():
    print("\nВведите координаты точек (X и Y через пробел). Можно использовать запятые.")
    print("Для завершения ввода введите 'q' или оставьте строку пустой.")
    x_list, y_list = [], []
    count = 1

    while True:
        user_input = input(f"Точка {count}: ").strip()
        if not user_input or user_input.lower() == 'q':
            break

        parts = user_input.split()
        if len(parts) != 2:
            print("  -> [ОШИБКА] Введите ровно ДВА числа через пробел!")
            continue

        try:
            x = parse_float(parts[0])
            y = parse_float(parts[1])
            x_list.append(x)
            y_list.append(y)
            count += 1
        except ValueError:
            print("  -> [ОШИБКА] Неверный формат! Используйте только цифры (например: -2.0 1,5).")

    return clean_and_sort_data(x_list, y_list)


def get_input_data():
    while True:
        print("\n=== ЛАБОРАТОРНАЯ РАБОТА №4 ===")
        print("Выберите способ ввода исходных данных (рекомендуется 10-12 точек):")
        print("1. Ввод из текстового файла")
        print("2. Ручной ввод из консоли")
        print("3. Сгенерировать файл 'data.txt' для Варианта 11 и выйти")

        choice = input("Ваш выбор (1/2/3): ").strip()

        if choice == '1':
            filename = input("Введите имя файла (нажмите Enter для 'data.txt'): ").strip()
            if not filename:
                filename = "data.txt"
            x_data, y_data = read_data_from_file(filename)
            if x_data is not None:
                return x_data, y_data

        elif choice == '2':
            x_data, y_data = read_data_from_console()
            if x_data is not None:
                return x_data, y_data

        elif choice == '3':
            x_d = np.arange(-2.0, 0.0 + 0.2 / 2, 0.2)
            y_d = original_function(x_d)
            np.savetxt("data.txt", np.column_stack((x_d, y_d)), header="X Y", comments="# ")
            print("\nФайл 'data.txt' успешно сгенерирован! Перезапустите программу и выберите пункт 1.")
            exit()
        else:
            print("[ОШИБКА] Неверный выбор. Введите 1, 2 или 3.")


def evaluate_approximations(x_data, y_data, functions_dict):
    results = {}
    best_func_name = None
    min_std_dev = float('inf')

    for name, func in functions_dict.items():
        try:
            popt, _ = curve_fit(func, x_data, y_data, maxfev=10000)
            y_pred = func(x_data, *popt)

            if np.isnan(y_pred).any() or np.isinf(y_pred).any():
                raise ValueError("Математически не определена на заданном интервале")

            S = np.sum((y_pred - y_data) ** 2)
            std_dev = np.sqrt(S / len(y_data))

            pearson_r = None
            if name == "Линейная":
                pearson_r = np.corrcoef(x_data, y_data)[0, 1]

            results[name] = {
                'success': True,
                'params': popt,
                'y_pred': y_pred,
                'S': S,
                'std_dev': std_dev,
                'pearson_r': pearson_r
            }

            if std_dev < min_std_dev:
                min_std_dev = std_dev
                best_func_name = name

        except Exception as e:
            results[name] = {
                'success': False,
                'error': str(e)
            }

    return results, best_func_name, min_std_dev


def print_results(x_data, y_data, results, best_func_name, min_std_dev):
    print("\n" + "=" * 50)
    print("ИСХОДНЫЕ ДАННЫЕ (ОТФИЛЬТРОВАННЫЕ):")
    for x, y in zip(x_data, y_data):
        print(f"X: {x:>5.2f} | Y: {y:>8.5f}")
    print("=" * 50)

    print("РЕЗУЛЬТАТЫ АППРОКСИМАЦИИ:")
    for name, data in results.items():
        if data['success']:
            print(f"\n{name}:")

            p = data['params']
            if name in ["Линейная", "Экспоненциальная", "Логарифмическая", "Степенная"]:
                params_str = f"a = {p[0]:.4f}, b = {p[1]:.4f}"
            elif name == "Полином 2-й степени":
                params_str = f"a0 = {p[0]:.4f}, a1 = {p[1]:.4f}, a2 = {p[2]:.4f}"
            elif name == "Полином 3-й степени":
                params_str = f"a0 = {p[0]:.4f}, a1 = {p[1]:.4f}, a2 = {p[2]:.4f}, a3 = {p[3]:.4f}"
            else:
                params_str = ", ".join([f"{val:.4f}" for val in p])

            print(f"  Коэффициенты: [{params_str}]")
            print(f"  Мера отклонения (S): {data['S']:.5f}")
            print(f"  Среднеквадратичное отклонение (σ): {data['std_dev']:.5f}")
            if data['pearson_r'] is not None:
                print(f"  Коэф. корреляции Пирсона (r): {data['pearson_r']:.5f}")
        else:
            print(f"\n{name}:\n  [ПРОПУСК] Функция математически не применима к данному набору точек.")

    print("=" * 50)
    if best_func_name:
        print(f"НАИЛУЧШАЯ АППРОКСИМИРУЮЩАЯ ФУНКЦИЯ: {best_func_name} (σ = {min_std_dev:.5f})")
    else:
        print("Не удалось подобрать ни одну аппроксимирующую функцию.")
    print("=" * 50 + "\n")


def plot_results_combined(x_data, y_data, results, best_func_name, functions_dict):
    x_min, x_max = np.min(x_data), np.max(x_data)
    margin = (x_max - x_min) * 0.2 if x_max != x_min else 1.0
    x_plot_wide = np.linspace(x_min - margin * 5, x_max + margin * 5, 2000)

    plt.figure("Combined Plot", figsize=(12, 8))
    plt.scatter(x_data, y_data, color='red', s=60, label='Узлы таблицы', zorder=5)
    plt.plot(x_plot_wide, original_function(x_plot_wide), 'k--', linewidth=2, alpha=0.6,
             label='Заданная функция y=5x/(x^4+7)')

    colors = ['blue', 'green', 'purple', 'orange', 'cyan', 'magenta']
    c_idx = 0

    for name, data in results.items():
        if not data['success']: continue
        popt = data['params']
        func = functions_dict[name]

        plot_x_safe = x_plot_wide[x_plot_wide > 1e-5] if name in ["Логарифмическая", "Степенная"] else x_plot_wide

        if len(plot_x_safe) > 0:
            y_plot_pred = func(plot_x_safe, *popt)
            lw = 3.5 if name == best_func_name else 2.0
            alpha = 1.0 if name == best_func_name else 0.8
            plt.plot(plot_x_safe, y_plot_pred, color=colors[c_idx % len(colors)],
                     linewidth=lw, alpha=alpha, label=f"{name} (S={data['S']:.3f})")
        c_idx += 1

    plt.title('Все аппроксимации на одном графике', fontsize=14, fontweight='bold')
    plt.xlabel('Ось X', fontsize=12)
    plt.ylabel('Ось Y', fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best', fontsize=10)

    plt.xlim(x_min - margin, x_max + margin)
    y_min_data, y_max_data = np.min(y_data), np.max(y_data)
    y_margin = (y_max_data - y_min_data) * 0.5 if y_max_data != y_min_data else 1.0
    plt.ylim(y_min_data - y_margin, y_max_data + y_margin)

    plt.savefig('approximation_plot_combined.png', dpi=300, bbox_inches='tight')


def plot_results_separate(x_data, y_data, results, best_func_name, functions_dict):
    success_results = {name: data for name, data in results.items() if data['success']}
    if not success_results:
        return

    n = len(success_results)
    cols = 2
    rows = (n + 1) // 2

    fig, axes = plt.subplots(rows, cols, figsize=(14, 6 * rows), num="Separate Plots")
    axes = np.atleast_1d(axes).flatten()

    x_min, x_max = np.min(x_data), np.max(x_data)
    margin = (x_max - x_min) * 0.2 if x_max != x_min else 1.0
    x_plot_wide = np.linspace(x_min - margin * 5, x_max + margin * 5, 2000)

    y_min_data, y_max_data = np.min(y_data), np.max(y_data)
    y_margin = (y_max_data - y_min_data) * 0.5 if y_max_data != y_min_data else 1.0

    colors = ['blue', 'green', 'purple', 'orange', 'cyan', 'magenta']

    for idx, (name, data) in enumerate(success_results.items()):
        ax = axes[idx]
        popt = data['params']
        func = functions_dict[name]

        ax.scatter(x_data, y_data, color='red', s=50, label='Узлы таблицы', zorder=5)
        ax.plot(x_plot_wide, original_function(x_plot_wide), 'k--', linewidth=2, alpha=0.5, label='Заданная функция')

        plot_x_safe = x_plot_wide[x_plot_wide > 1e-5] if name in ["Логарифмическая", "Степенная"] else x_plot_wide

        if len(plot_x_safe) > 0:
            y_plot_pred = func(plot_x_safe, *popt)
            lw = 3.5 if name == best_func_name else 2.5
            title_prefix = "★ НАИЛУЧШАЯ: " if name == best_func_name else ""

            ax.plot(plot_x_safe, y_plot_pred, color=colors[idx % len(colors)],
                    linewidth=lw, label=f"Аппроксимация (S={data['S']:.3f})")
            ax.set_title(f"{title_prefix}{name}", fontsize=12, fontweight='bold')

        ax.set_xlabel('Ось X', fontsize=10)
        ax.set_ylabel('Ось Y', fontsize=10)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best', fontsize=9)

        ax.set_xlim(x_min - margin, x_max + margin)
        ax.set_ylim(y_min_data - y_margin, y_max_data + y_margin)

    for i in range(n, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.savefig('approximation_plot_separate.png', dpi=300, bbox_inches='tight')


if __name__ == "__main__":
    x_input, y_input = get_input_data()

    num_points = len(x_input)
    if num_points < 10 or num_points > 12:
        print(f"\n[ВНИМАНИЕ] Согласно заданию, таблица должна содержать от 10 до 12 точек!")
        print(f"Вы предоставили {num_points} точек. Программа продолжит работу, но это нарушает п. 4.a.")

    funcs_to_test = {
        "Линейная": linear_func,
        "Полином 2-й степени": poly2_func,
        "Полином 3-й степени": poly3_func,
        "Экспоненциальная": exp_func,
        "Логарифмическая": log_func,
        "Степенная": power_func
    }

    eval_results, best_name, min_std = evaluate_approximations(x_input, y_input, funcs_to_test)

    print_results(x_input, y_input, eval_results, best_name, min_std)

    while True:
        print("Выберите способ отображения графиков:")
        print("1. Все функции на одном графике")
        print("2. Каждая функция на отдельном графике (сетка)")
        print("3. Показать оба варианта")
        plot_choice = input("Ваш выбор (1/2/3): ").strip()

        if plot_choice in ['1', '2', '3']:
            break
        print("[ОШИБКА] Введите 1, 2 или 3.")

    if plot_choice in ['1', '3']:
        plot_results_combined(x_input, y_input, eval_results, best_name, funcs_to_test)

    if plot_choice in ['2', '3']:
        plot_results_separate(x_input, y_input, eval_results, best_name, funcs_to_test)

    plt.show()