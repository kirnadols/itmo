import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 0.8 * np.sin(1.5 * x) + 0.6 * np.sin(3.2 * x) + 0.4 * np.sin(5.7 * x) + 0.2 * np.sin(8.1 * x)

def golden_section_max_history(a, b, eps):
    history = [(a, b)]
    resphi = 2 - (1 + np.sqrt(5)) / 2

    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    y1, y2 = f(x1), f(x2)

    iters = 0
    print(f"Поиск максимума на промежутке [{a}, {b}] с точностью {eps}\n")

    while abs(b - a) > eps:
        iters += 1

        if y1 < y2:
            a = x1
            x1 = x2
            y1 = y2
            x2 = b - resphi * (b - a)
            y2 = f(x2)
        else:
            b = x2
            x2 = x1
            y2 = y1
            x1 = a + resphi * (b - a)
            y1 = f(x1)

        history.append((a, b))

        if iters <= 3:
            print(f"Итерация {iters}: Отрезок сузился до [{a:.4f}, {b:.4f}]")

    x_opt = (a + b) / 2
    print(f"\nИтог: Максимум x* ≈ {x_opt:.5f}, f(x*) ≈ {f(x_opt):.5f}, всего итераций: {iters}")
    return history, x_opt

eps = 0.001
a0, b0 = 0.0, 0.6
history, x_max = golden_section_max_history(a0, b0, eps)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

x_full = np.linspace(-1, 1.5, 1000)
ax1.plot(x_full, f(x_full), 'k-', label='f(x)')
ax1.axvspan(a0, b0, color='red', alpha=0.15, label=f'Промежуток унимодальности: [{a0}, {b0}]')
ax1.scatter([x_max], [f(x_max)], color='red', s=80, zorder=5, label='Найденный максимум')

ax1.set_title('Локальный максимум на отрезке [0.0, 0.6]')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

for i, (a, b) in enumerate(history):
    ax2.plot([a, b], [i, i], color='red', marker='|', markersize=8, linewidth=2)
    if i % 2 == 0 or i == len(history) - 1:
        ax2.text(b + 0.005, i, f'Итерация {i}: [{a:.4f}, {b:.4f}]', va='center', fontsize=9)

ax2.set_title('Визуализация сужения отрезка (Метод золотого сечения - Максимум)')
ax2.set_xlabel('x')
ax2.set_ylabel('Номер итерации')
ax2.set_xlim(a0 - 0.05, b0 + 0.15)
ax2.invert_yaxis()
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()