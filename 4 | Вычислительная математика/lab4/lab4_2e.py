import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return (5 * x) / (x**4 + 7)

x_data = np.arange(-2.0, 0.1, 0.2)
x_data[-1] = 0.0
y_data = f(x_data)

coeff_lin = np.polyfit(x_data, y_data, 1)
coeff_quad = np.polyfit(x_data, y_data, 2)
coeff_cub = np.polyfit(x_data, y_data, 3)

x_smooth = np.linspace(-2.0, 0.0, 100)
y_lin = np.polyval(coeff_lin, x_smooth)
y_quad = np.polyval(coeff_quad, x_smooth)
y_cub = np.polyval(coeff_cub, x_smooth)

plt.figure(figsize=(11, 7))

plt.plot(x_data, y_data, 'ro', markersize=7, label='Заданная функция (узлы)', zorder=5)

plt.plot(x_smooth, y_lin, '-', color='blue', linewidth=2, alpha=0.8, label='Линейная функция')
plt.plot(x_smooth, y_quad, '-', color='green', linewidth=2, alpha=0.8, label='Квадратичная функция')
plt.plot(x_smooth, y_cub, '-', color='purple', linewidth=2, alpha=0.8, label='Кубическая функция')

plt.title('Графики всех эмпирических функций (Пункт 2e)', fontsize=14, pad=15)
plt.xlabel('Ось X', fontsize=12)
plt.ylabel('Ось Y', fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.text(-1.95, -0.05,
         "Примечание:\nЛогарифмическая, степенная\nи экспоненциальная модели\nнеприменимы (x <= 0, y <= 0)",
         fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

plt.legend(loc='lower right', fontsize=11)
plt.tight_layout()
plt.show()