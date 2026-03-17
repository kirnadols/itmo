import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def f(x):
    return 0.8 * np.sin(1.5 * x) + 0.6 * np.sin(3.2 * x) + 0.4 * np.sin(5.7 * x) + 0.2 * np.sin(8.1 * x)


def df(x):
    return 1.2 * np.cos(1.5 * x) + 1.92 * np.cos(3.2 * x) + 2.28 * np.cos(5.7 * x) + 1.62 * np.cos(8.1 * x)


def d2f(x):
    return -1.8 * np.sin(1.5 * x) - 6.144 * np.sin(3.2 * x) - 12.996 * np.sin(5.7 * x) - 13.122 * np.sin(8.1 * x)


def newton_method(x0, eps=0.001):
    x = x0
    for _ in range(100):
        if abs(df(x)) <= eps:
            break
        x = x - df(x) / d2f(x)
    return x


def dichotomy_history(a, b, eps, find_max):
    history = [(a, b)]
    delta = eps / 2.0
    while (b - a) > 2 * eps:
        x1 = (a + b) / 2 - delta
        x2 = (a + b) / 2 + delta
        y1, y2 = f(x1), f(x2)
        if find_max:
            if y1 < y2:
                a = x1
            else:
                b = x2
        else:
            if y1 > y2:
                a = x1
            else:
                b = x2
        history.append((a, b))
    return history


eps = 0.001
x_vals = np.linspace(-5, 3, 2000)
df_vals = df(x_vals)

extrema_x_rough = []
extrema_type_rough = []

for i in range(len(x_vals) - 1):
    if df_vals[i] * df_vals[i + 1] < 0:
        x_start = (x_vals[i] + x_vals[i + 1]) / 2
        x_ext = newton_method(x_start, eps)
        ext_type = "Максимум" if d2f(x_ext) < 0 else "Минимум"
        extrema_x_rough.append(x_ext)
        extrema_type_rough.append(ext_type)

boundaries = [-5.0]
for i in range(len(extrema_x_rough) - 1):
    boundaries.append((extrema_x_rough[i] + extrema_x_rough[i + 1]) / 2)
boundaries.append(3.0)

histories = []
for i in range(len(extrema_x_rough)):
    a = boundaries[i]
    b = boundaries[i + 1]
    find_max = (extrema_type_rough[i] == "Максимум")
    histories.append(dichotomy_history(a, b, eps, find_max))

max_len = max(len(h) for h in histories)
for h in histories:
    while len(h) < max_len:
        h.append(h[-1])

fig, ax = plt.subplots(figsize=(14, 7))


def update(frame):
    ax.clear()
    ax.plot(x_vals, f(x_vals), color='black', linewidth=1.5)

    for i, h in enumerate(histories):
        a, b = h[frame]
        is_max = (extrema_type_rough[i] == "Максимум")
        color = 'red' if is_max else 'blue'
        ax.axvspan(a, b, color=color, alpha=0.4)

        mid = (a + b) / 2
        ax.scatter([mid], [f(mid)], color=color, s=30, zorder=5)

    ax.set_title(f'Метод дихотомии. Итерация: {frame}')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_xlim(-5, 3)
    ax.set_ylim(-2, 2.5)
    ax.grid(True, linestyle='--', alpha=0.5)


ani = FuncAnimation(fig, update, frames=max_len, repeat=True)
ani.save('dichotomy_animation.gif', writer=PillowWriter(fps=2))