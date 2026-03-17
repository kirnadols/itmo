import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 0.8 * np.sin(1.5 * x) + 0.6 * np.sin(3.2 * x) + 0.4 * np.sin(5.7 * x) + 0.2 * np.sin(8.1 * x)

def df(x):
    return 1.2 * np.cos(1.5 * x) + 1.92 * np.cos(3.2 * x) + 2.28 * np.cos(5.7 * x) + 1.62 * np.cos(8.1 * x)


def chord_method_history(a, b, eps):
    history = [(a, b)]
    secants = []
    iters = 0

    print(f"Поиск минимума методом хорд на [{a}, {b}] с точностью {eps}\n")

    while True:
        iters += 1
        fa, fb = df(a), df(b)

        x_new = a - fa * (a - b) / (fa - fb)
        secants.append(([a, b], [fa, fb]))

        df_new = df(x_new)

        if iters <= 3:
            print(f"Итерация {iters}: x~ = {x_new:.5f}, f'(x~) = {df_new:.5f}")

        if abs(df_new) <= eps or iters > 100:
            history.append((a, b))
            x_opt = x_new
            break

        if df_new > 0:
            b = x_new
        else:
            a = x_new

        history.append((a, b))

    print(f"\nИтог: Минимум x* ≈ {x_opt:.5f}, f(x*) ≈ {f(x_opt):.5f}, всего итераций: {iters}")
    return history, secants, x_opt


eps = 0.001
a0, b0 = 1.0, 2.0
history, secants, x_min = chord_method_history(a0, b0, eps)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16))

x_full = np.linspace(-5, 3, 2000)
ax1.plot(x_full, f(x_full), 'k-', label='f(x)')
ax1.axvspan(a0, b0, color='blue', alpha=0.15, label=f'Промежуток: [{a0}, {b0}]')
ax1.scatter([x_min], [f(x_min)], color='blue', s=80, zorder=5, label='Найденный минимум')
ax1.set_title('Локальный минимум функции f(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

# Средний график: Производная f'(x) и секущие (хорды)
x_zoom = np.linspace(a0 - 0.1, b0 + 0.1, 500)
ax2.plot(x_zoom, df(x_zoom), 'g-', linewidth=2, label="f'(x) (Производная)")
ax2.axhline(0, color='black', linewidth=1)  # Ось ОХ

colors = plt.cm.viridis(np.linspace(0, 0.8, len(secants)))
for i, (xs, ys) in enumerate(secants):
    ax2.plot(xs, ys, marker='o', linestyle='--', color=colors[i], label=f'Хорда {i + 1}')

ax2.scatter([x_min], [0], color='red', s=80, zorder=5, label="Корень f'(x)=0")
ax2.set_title("Поиск корня производной f'(x)=0 методом хорд")
ax2.set_xlabel('x')
ax2.set_ylabel("f'(x)")
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

for i, (a, b) in enumerate(history):
    ax3.plot([a, b], [i, i], color='blue', marker='|', markersize=8, linewidth=2)
    ax3.text(b + 0.01, i, f'Ит. {i}: [{a:.4f}, {b:.4f}]', va='center', fontsize=9)

ax3.set_title('Визуализация сужения отрезка (Метод хорд)')
ax3.set_xlabel('x')
ax3.set_ylabel('Номер итерации')
ax3.set_xlim(a0 - 0.05, b0 + 0.3)
ax3.invert_yaxis()
ax3.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()