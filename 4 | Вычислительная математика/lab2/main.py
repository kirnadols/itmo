import numpy as np
import matplotlib.pyplot as plt
import requests

from equations import EQUATIONS, SYSTEMS
from methods import verify_interval, chord_method, secant_method, simple_iteration_method, newton_system

ZVONOK_API_KEY = "40e1143e58bfb01880b5b291fa1110f0"
ZVONOK_CAMPAIGN_ID = "885474916"


def send_voice_message(phone_number, text):
    url = "https://zvonok.com/manager/cabapi_external/api/v1/phones/call/"

    payload = {
        "public_key": ZVONOK_API_KEY,
        "phone": phone_number,
        "campaign_id": ZVONOK_CAMPAIGN_ID,
        "text": text
    }

    print("Отправка запроса на звонок...")
    try:
        response = requests.post(url, data=payload)

        try:
            result = response.json()
            if response.status_code == 200 and result.get('status') == 'ok' or result.get('status') == 'success':
                print(
                    f"Успех! Звонок на номер {phone_number} инициирован. ID звонка: {result.get('call_id', 'неизвестно')}")
            else:
                print(f"{result.get('data', result)}")
        except ValueError:
            print(f"Ошибка HTTP {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сетевого соединения: {e}")


def safe_float_input(prompt, positive_only=False):
    while True:
        val_str = input(prompt).strip().replace(',', '.')
        try:
            val = float(val_str)
            if positive_only and val <= 0:
                print("Ошибка: значение должно быть строго больше нуля!")
                continue
            return val
        except ValueError:
            print("Ошибка: нужно ввести число (например, 1.5 или -2). Попробуйте снова.")


def safe_choice_input(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Ошибка: выберите один из предложенных вариантов: {', '.join(valid_choices)}")


def plot_function(f, a, b, title):
    x = np.linspace(a - 1, b + 1, 400)
    y = f(x)
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'b', label="f(x)")
    plt.axvline(a, color='r', linestyle='--', label=f'Граница a={a}')
    plt.axvline(b, color='g', linestyle='--', label=f'Граница b={b}')
    plt.axhline(0, color='black', linewidth=1)
    plt.grid(True)
    plt.legend()
    plt.title(title)
    plt.show()


def plot_system(sys_dict):
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x, y)

    Z1 = sys_dict["f1"](X, Y)
    Z2 = sys_dict["f2"](X, Y)

    plt.figure(figsize=(8, 5))
    plt.contour(X, Y, Z1, levels=[0], colors='blue')
    plt.contour(X, Y, Z2, levels=[0], colors='red')
    plt.grid(True)
    plt.title("График системы нелинейных уравнений (пересечение = корни)")
    plt.plot([], [], color='blue', label='Уравнение 1')
    plt.plot([], [], color='red', label='Уравнение 2')
    plt.legend()
    plt.show()


def get_input():
    choice = safe_choice_input("Ввод данных: 1 - Клавиатура, 2 - Файл (input.txt): ", ['1', '2'])
    if choice == '2':
        try:
            with open("input.txt", "r") as f:
                data = f.read().split()
                if len(data) < 3:
                    raise ValueError("В файле недостаточно данных (нужно 3 числа: a, b, eps).")
                a = float(data[0].replace(',', '.'))
                b = float(data[1].replace(',', '.'))
                eps = float(data[2].replace(',', '.'))
                if eps <= 0:
                    raise ValueError("Погрешность eps должна быть больше нуля.")
                print(f"Данные из файла успешно загружены: a={a}, b={b}, eps={eps}")
                return a, b, eps
        except Exception as e:
            print(f"Ошибка чтения файла: {e}\nПереходим на ручной ввод.")

    a = safe_float_input("Введите левую границу (a): ")
    b = safe_float_input("Введите правую границу (b): ")
    eps = safe_float_input("Введите погрешность (eps): ", positive_only=True)
    return a, b, eps


def save_or_print(text, voice_text=None):
    print("\n" + text)
    choice = safe_choice_input("Сохранить результат в файл? (y/n): ", ['y', 'n', 'Y', 'N', 'н', 'Н', 'т', 'Т']).lower()
    if choice in ['y', 'н']:
        with open("output.txt", "w", encoding='utf-8') as f:
            f.write(text)
        print("Результат сохранен в output.txt")

    if voice_text:
        call_choice = safe_choice_input("Озвучить результат по телефону? (y/n): ",
                                        ['y', 'n', 'Y', 'N', 'н', 'Н', 'т', 'Т']).lower()
        if call_choice in ['y', 'н']:
            phone = input("Введите номер телефона (в формате +79991234567): ").strip()
            phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            send_voice_message(phone, voice_text)


def main():
    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Решение одного нелинейного уравнения")
        print("2. Решение системы нелинейных уравнений")
        print("0. Выход")
        mode = safe_choice_input("Выберите режим: ", ['0', '1', '2'])

        if mode == '0':
            print("Выход из программы. До свидания!")
            break

        if mode == '1':
            print("\nВыберите уравнение:")
            valid_eq_keys = []
            for k, v in EQUATIONS.items():
                print(f"{k}. {v['str']}")
                valid_eq_keys.append(str(k))

            eq_idx = int(safe_choice_input("Номер уравнения: ", valid_eq_keys))
            func = EQUATIONS[eq_idx]["func"]

            a, b, eps = get_input()
            if a >= b:
                print("Ошибка: Левая граница 'a' должна быть строго меньше правой 'b'. Начните заново.")
                continue

            is_valid, msg = verify_interval(func, a, b)
            print(f"\nВерификация интервала: {msg}")
            if not is_valid: continue

            plot_function(func, a, b, EQUATIONS[eq_idx]["str"])

            print("\nВыберите метод:")
            print("2. Метод хорд\n4. Метод секущих\n5. Метод простой итерации")
            method_idx = safe_choice_input("Номер метода: ", ['2', '4', '5'])

            out_text = ""
            root = None
            hist = []

            if method_idx == '2':
                root, hist = chord_method(func, a, b, eps)
                out_text += "--- Метод хорд ---\n"
                out_text += f"{'№':<5} | {'x_i':<10} | {'f(x_i)':<12} | {'|x_i - x_{i-1}|':<15}\n"
                for row in hist: out_text += f"{row[0]:<5} | {row[1]:<10.5f} | {row[2]:<12.5f} | {row[3]:<15.5f}\n"
                out_text += f"\nКорень: {root:.5f}, f(x) = {func(root):.5f}, Итераций: {len(hist)}"

            elif method_idx == '4':
                root, hist = secant_method(func, a, b, eps)
                out_text += "--- Метод секущих ---\n"
                out_text += f"{'№':<5} | {'x_i':<10} | {'f(x_i)':<12} | {'diff':<10}\n"
                for row in hist: out_text += f"{row[0]:<5} | {row[1]:<10.5f} | {row[2]:<12.5f} | {row[3]:<10.5f}\n"
                out_text += f"\nКорень: {root:.5f}, f(x) = {func(root):.5f}, Итераций: {len(hist)}"

            elif method_idx == '5':
                root, hist, q_msg = simple_iteration_method(func, a, b, eps)
                out_text += f"--- Метод простой итерации ---\n{q_msg}\n"
                out_text += f"{'№':<5} | {'x_curr':<10} | {'x_next':<10} | {'phi(x)':<12} | {'f(x)':<12} | {'diff':<10}\n"
                for row in hist: out_text += f"{row[0]:<5} | {row[1]:<10.5f} | {row[2]:<10.5f} | {row[3]:<12.5f} | {row[4]:<12.5f} | {row[5]:<10.5f}\n"
                out_text += f"\nКорень: {root:.5f}, f(x) = {func(root):.5f}, Итераций: {len(hist)}"

            if root is not None:
                safe_root = str(round(root, 3)).replace('-', 'минус ')
                voice_summary = f"Привит. Це я вычислительная математика. Восстание машин уже близко. Вычисление завершено. Найден корень: {safe_root}. Потребовалось итераций: {len(hist)}."
                save_or_print(out_text, voice_summary)
            else:
                save_or_print(out_text)

        elif mode == '2':
            print("\nВыберите систему уравнений:")
            valid_sys_keys = []
            for k, v in SYSTEMS.items():
                print(f"--- Система {k} ---\n{v['str']}")
                valid_sys_keys.append(str(k))

            sys_idx = int(safe_choice_input("\nНомер системы: ", valid_sys_keys))
            cur_sys = SYSTEMS[sys_idx]

            plot_system(cur_sys)

            print("Введите начальные приближения с клавиатуры (см. график):")
            x0 = safe_float_input("x0 = ")
            y0 = safe_float_input("y0 = ")
            eps = safe_float_input("Введите погрешность (eps): ", positive_only=True)

            ans, hist = newton_system(cur_sys, x0, y0, eps)

            out_text = "--- Метод Ньютона для систем ---\n"
            out_text += f"{'№':<5} | {'x_i':<10} | {'y_i':<10} | {'погрешность_x':<15} | {'погрешность_y':<15}\n"
            for row in hist:
                out_text += f"{row[0]:<5} | {row[1]:<10.5f} | {row[2]:<10.5f} | {row[3]:<15.5f} | {row[4]:<15.5f}\n"

            x_res, y_res = ans
            out_text += f"\nВектор неизвестных: x1 = {x_res:.5f}, x2 = {y_res:.5f}\n"
            out_text += f"Количество итераций: {len(hist)}\n"
            out_text += f"Вектор погрешностей (последний шаг): |dx| = {hist[-1][3]:.5f}, |dy| = {hist[-1][4]:.5f}\n"

            r1 = cur_sys["f1"](x_res, y_res)
            r2 = cur_sys["f2"](x_res, y_res)
            out_text += f"Проверка: f1(x,y) = {r1:.7f}, f2(x,y) = {r2:.7f}"

            safe_x = str(round(x_res, 5)).replace('-', 'минус ')
            safe_y = str(round(y_res, 5)).replace('-', 'минус ')
            voice_summary = f"Решение системы найдено. Икс равен {safe_x}, игрек равен {safe_y}. Количество шагов: {len(hist)}."

            save_or_print(out_text, voice_summary)


if __name__ == "__main__":
    main()