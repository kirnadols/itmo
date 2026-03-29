import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Целевая функция
def f(x):
    return 0.25 * x ** 4 + x ** 2 - 8 * x + 12


# Модифицированная функция с сохранением истории итераций
def powell_history(f, x1, delta_x, eps1, eps2, max_iter=100):
    step_2 = True
    history = []

    for k in range(1, max_iter + 1):
        if step_2:
            x2 = x1 + delta_x
            f1, f2 = f(x1), f(x2)
            if f1 > f2:
                x3 = x1 + 2 * delta_x
            else:
                x3 = x1 - delta_x
            f3 = f(x3)
        else:
            f1, f2, f3 = f(x1), f(x2), f(x3)

        candidates = [(x1, f1), (x2, f2), (x3, f3)]
        x_min, f_min = min(candidates, key=lambda t: t[1])

        num = (x2 ** 2 - x3 ** 2) * f1 + (x3 ** 2 - x1 ** 2) * f2 + (x1 ** 2 - x2 ** 2) * f3
        den = (x2 - x3) * f1 + (x3 - x1) * f2 + (x1 - x2) * f3

        if abs(den) < 1e-15:
            x1 = x_min
            step_2 = True
            continue

        x_bar = 0.5 * num / den
        f_bar = f(x_bar)

        # Сохраняем данные текущего шага для анимации
        history.append({
            'iter': k,
            'points': (x1, x2, x3),
            'x_bar': x_bar
        })

        cond1 = abs((f_min - f_bar) / f_bar) < eps1
        cond2 = abs((x_min - x_bar) / x_bar) < eps2

        if cond1 and cond2:
            break

        interval_min = min(x1, x2, x3)
        interval_max = max(x1, x2, x3)

        if interval_min <= x_bar <= interval_max:
            points = [(x1, f1), (x2, f2), (x3, f3), (x_bar, f_bar)]
            points.sort(key=lambda t: t[0])
            best_idx = min(range(4), key=lambda i: points[i][1])

            if best_idx == 0:
                new_points = points[0:3]
            elif best_idx == 3:
                new_points = points[1:4]
            else:
                new_points = points[best_idx - 1: best_idx + 2]

            x1, x2, x3 = new_points[0][0], new_points[1][0], new_points[2][0]
            step_2 = False
        else:
            x1 = x_bar
            step_2 = True

    return history


# ==========================================
# НАСТРОЙКА И ЗАПУСК АНИМАЦИИ
# ==========================================

# 1. Получаем историю итераций
x1_start = 1.0
delta_x_start = 0.25
eps = 0.0001
history = powell_history(f, x1_start, delta_x_start, eps, eps)

# 2. Настраиваем график
fig, ax = plt.subplots(figsize=(10, 6))
x_vals = np.linspace(-0.5, 3.5, 400)
y_vals = f(x_vals)

# Рисуем саму функцию f(x)
ax.plot(x_vals, y_vals, label='f(x) = 0.25x^4 + x^2 - 8x + 12', color='black', linewidth=2)

# Пустые объекты, которые мы будем обновлять в анимации
parabola_line, = ax.plot([], [], '--', color='orange', label='Аппроксимирующая парабола q(x)')
points_scatter = ax.scatter([], [], color='blue', s=80, zorder=5, label='Опорные точки (x1, x2, x3)')
xbar_scatter = ax.scatter([], [], color='red', s=100, marker='*', zorder=6, label='Минимум параболы (x*)')
vline = ax.axvline(0, color='red', linestyle=':', alpha=0)

ax.set_xlim(-0.5, 3.5)
ax.set_ylim(-2, 15)
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
title = ax.set_title('Метод квадратичной аппроксимации')
ax.legend()
ax.grid(True)


# 3. Функция обновления кадров
def update(frame):
    state = history[frame]
    x_points = state['points']
    x_bar = state['x_bar']
    y_points = [f(x) for x in x_points]

    # Строим полином 2-й степени через 3 точки
    coeffs = np.polyfit(x_points, y_points, 2)
    p = np.poly1d(coeffs)

    # Генерируем точки для отрисовки параболы
    x_p = np.linspace(min(x_points) - 0.5, max(x_points) + 0.5, 100)
    y_p = p(x_p)

    parabola_line.set_data(x_p, y_p)
    points_scatter.set_offsets(np.column_stack((x_points, y_points)))
    xbar_scatter.set_offsets(np.column_stack(([x_bar], [f(x_bar)])))

    vline.set_xdata([x_bar, x_bar])
    vline.set_alpha(0.5)

    title.set_text(f"Итерация {state['iter']}: x* = {x_bar:.5f}")
    return parabola_line, points_scatter, xbar_scatter, vline, title


# 4. Создаем анимацию
ani = FuncAnimation(fig, update, frames=len(history), interval=1500, blit=False, repeat_delay=3000)

print(f"Анимация готова! Всего итераций: {len(history)}")

# Сохраняем в GIF (раскомментируйте, если нужно сохранить)
# ani.save('powell_animation.gif', writer='pillow', fps=1)

# Показываем окно
plt.show()