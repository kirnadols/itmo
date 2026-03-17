import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 0.8 * np.sin(1.5 * x) + 0.6 * np.sin(3.2 * x) + 0.4 * np.sin(5.7 * x) + 0.2 * np.sin(8.1 * x)

def df(x):
    return 1.2 * np.cos(1.5 * x) + 1.92 * np.cos(3.2 * x) + 2.28 * np.cos(5.7 * x) + 1.62 * np.cos(8.1 * x)

def d2f(x):
    return -1.8 * np.sin(1.5 * x) - 6.144 * np.sin(3.2 * x) - 12.996 * np.sin(5.7 * x) - 13.122 * np.sin(8.1 * x)

def newton_method_max_history(x0, eps):
    history = [x0]
    tangents = []
    x = x0
    iters = 0

    print(f"Поиск максимума методом Ньютона. Стартовая точка x0 = {x0}, точность {eps}\n")

    while True:
        iters += 1
        dfx = df(x)
        d2fx = d2f(x)

        x_new = x - dfx / d2fx

        tangents.append((x, dfx, x_new))

        if iters <= 3:
            print(
                f"Итерация {iters}: x_{iters - 1} = {x:.5f}, f'(x) = {dfx:.5f}, f''(x) = {d2fx:.5f} -> x_{iters} = {x_new:.5f}")

        if abs(df(x_new)) <= eps or iters > 100:
            history.append(x_new)
            x_opt = x_new
            break

        x = x_new
        history.append(x)

    print(f"\nИтог: Максимум x* ≈ {x_opt:.5f}, f(x*) ≈ {f(x_opt):.5f}, всего итераций: {iters}")
    return history, tangents, x_opt


eps = 0.001
x_start = 0.2
a0, b0 = 0.0, 0.6
history, tangents, x_max = newton_method_max_history(x_start, eps)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16))

x_full = np.linspace(-1, 1.5, 1000)
ax1.plot(x_full, f(x_full), 'k-', label='f(x)')
ax1.axvspan(a0, b0, color='red', alpha=0.15, label=f'Рассматриваемый промежуток: [{a0}, {b0}]')

for i, x_val in enumerate(history):
    alpha_val = max(0.3, i / len(history))
    ax1.scatter([x_val], [f(x_val)], color='red', alpha=alpha_val, s=60, zorder=5)

ax1.scatter([x_max], [f(x_max)], color='yellow', edgecolors='black', s=100, zorder=6, label='Найденный максимум')
ax1.set_title('Локальный максимум функции f(x) (Метод Ньютона)')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

x_zoom = np.linspace(0.1, 0.5, 500)
ax2.plot(x_zoom, df(x_zoom), 'g-', linewidth=2, label="f'(x) (Производная)")
ax2.axhline(0, color='black', linewidth=1)

colors = plt.cm.plasma(np.linspace(0, 0.8, len(tangents)))
for i, (x_k, dfx_k, x_new) in enumerate(tangents):
    ax2.plot([x_k, x_new], [dfx_k, 0], marker='o', linestyle='--', color=colors[i], label=f'Касательная {i + 1}')

ax2.scatter([x_max], [0], color='red', s=80, zorder=5, label="Корень f'(x)=0")
ax2.set_title("Поиск корня производной f'(x)=0 касательными (для максимума)")
ax2.set_xlabel('x')
ax2.set_ylabel("f'(x)")
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

iterations = range(len(history))
ax3.plot(iterations, history, color='red', marker='o', linestyle='-', linewidth=2, markersize=8)
for i, x_val in enumerate(history):
    ax3.text(i, x_val + 0.01, f'{x_val:.4f}', ha='center', fontsize=9)

ax3.axhline(x_max, color='blue', linestyle='--', alpha=0.5, label='Истинный максимум')
ax3.set_title('Траектория приближения к точке максимума $x^*$')
ax3.set_xlabel('Номер итерации')
ax3.set_ylabel('Значение x')
ax3.set_xticks(iterations)
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.legend()

plt.tight_layout()
plt.show()