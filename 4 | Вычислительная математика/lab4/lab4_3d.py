import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return (5 * x) / (x**4 + 7)

x_data = np.arange(-2.0, 0.1, 0.2)
x_data[-1] = 0.0
y_data = f(x_data)

coeff_lin = np.polyfit(x_data, y_data, 1)

coeff_quad = np.polyfit(x_data, y_data, 2)

x_smooth = np.linspace(-2.0, 0.0, 100)
y_lin_smooth = np.polyval(coeff_lin, x_smooth)
y_quad_smooth = np.polyval(coeff_quad, x_smooth)

plt.figure(figsize=(10, 6))

plt.plot(x_data, y_data, 'ro', markersize=7, label='Заданная функция (узлы)', zorder=5)

plt.plot(x_smooth, y_lin_smooth, '-', color='blue', linewidth=2, alpha=0.8,
         label=f'Линейное: y = {coeff_lin[0]:.3f}x + {coeff_lin[1]:.3f}')
plt.plot(x_smooth, y_quad_smooth, '-', color='green', linewidth=2, alpha=0.8,
         label=f'Квадратичное: y = {coeff_quad[0]:.3f}x² + {coeff_quad[1]:.3f}x + {coeff_quad[2]:.3f}')

plt.title('Линейное и квадратичное приближение', fontsize=14, pad=15)
plt.xlabel('Ось X', fontsize=12)
plt.ylabel('Ось Y', fontsize=12)

plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

plt.legend(loc='lower right', fontsize=11, framealpha=0.9)

plt.tight_layout()
plt.show()