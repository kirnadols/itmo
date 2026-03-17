import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 0.8 * np.sin(1.5 * x) + 0.6 * np.sin(3.2 * x) + 0.4 * np.sin(5.7 * x) + 0.2 * np.sin(8.1 * x)


def bisection_max_history(a, b, eps):
    history = [(a, b)]
    delta = eps / 2.0
    iters = 0

    print(f"Поиск максимума на промежутке [{a}, {b}] с точностью {eps}\n")

    while (b - a) > 2 * eps:
        iters += 1
        x1 = (a + b) / 2 - delta
        x2 = (a + b) / 2 + delta
        y1, y2 = f(x1), f(x2)

        if y1 < y2:
            a = x1
        else:
            b = x2

        history.append((a, b))

        if iters <= 3:
            print(f"Итерация {iters}: x1={x1:.5f}, x2={x2:.5f} | y1={y1:.5f}, y2={y2:.5f}")
            print(f" -> Новый отрезок: [{a:.5f}, {b:.5f}]\n")

    x_max = (a + b) / 2
    print(f"Итог: Максимум x* ≈ {x_max:.5f}, f(x*) ≈ {f(x_max):.5f}, всего итераций: {iters}")
    return history, x_max


a0, b0 = 0.0, 0.6
eps = 0.001
history, x_max = bisection_max_history(a0, b0, eps)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

x_full = np.linspace(-1, 1.5, 1000)
ax1.plot(x_full, f(x_full), 'k-', label='f(x)')
ax1.axvspan(a0, b0, color='red', alpha=0.15, label=f'Промежуток унимодальности: [{a0}, {b0}]')
ax1.scatter([x_max], [f(x_max)], color='red', s=80, zorder=5, label='Найденный максимум')
ax1.set_title('Локальный максимум на отрезке [0, 0.6]')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.grid(True, linestyle='--')
ax1.legend()

for i, (a, b) in enumerate(history):
    ax2.plot([a, b], [i, i], color='red', marker='|', markersize=8, linewidth=2)

ax2.set_title('Визуализация сужения отрезка (Поиск максимума)')
ax2.set_xlabel('x')
ax2.set_ylabel('Номер итерации')
ax2.set_xlim(a0 - 0.05, b0 + 0.05)
ax2.invert_yaxis()
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()