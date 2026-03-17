import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 0.8 * np.sin(1.5 * x) + 0.6 * np.sin(3.2 * x) + 0.4 * np.sin(5.7 * x) + 0.2 * np.sin(8.1 * x)


def bisection_history(a, b, eps, find_max=False):
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
a0, b0 = 1.0, 2.0
history = bisection_history(a0, b0, eps, find_max=False)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

x_full = np.linspace(-5, 3, 2000)
ax1.plot(x_full, f(x_full), 'k-', label='f(x)')
ax1.axvspan(a0, b0, color='blue', alpha=0.15, label=f'Начальный отрезок: [{a0}, {b0}]')
ax1.set_title('Функция f(x) на отрезке [-5, 3]')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

for i, (a, b) in enumerate(history):
    ax2.plot([a, b], [i, i], color='blue', marker='|', markersize=8, linewidth=2)
    if i % 2 == 0 or i == len(history) - 1:
        ax2.text(b + 0.01, i, f'Итерация {i}: [{a:.4f}, {b:.4f}]', va='center', fontsize=9)

ax2.set_title('Визуализация сужения отрезка (Метод деления пополам)')
ax2.set_xlabel('x')
ax2.set_ylabel('Номер итерации')
ax2.set_xlim(a0 - 0.05, b0 + 0.2)
ax2.invert_yaxis()
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()