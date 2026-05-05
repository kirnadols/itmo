import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

# ==============================================================================
# ИСХОДНЫЕ ДАННЫЕ (ВАРИАНТ 12)
# ==============================================================================
data = np.array([
    [1.00, 1.18, 0.23],
    [1.94, 2.05, 2.02],
    [3.01, 3.04, 3.79],
    [3.98, 4.17, 0.92],
    [5.07, 4.95, 0.01]
])

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]

print("="*50)
print("ИСХОДНЫЕ ДАННЫЕ")
print("="*50)
for i in range(len(X)):
    print(f"Точка {i}: x={X[i]:.2f}, y={Y[i]:.2f}, z={Z[i]:.2f}")

# ==============================================================================
# ЗАДАНИЕ 1: ДВУМЕРНАЯ ГАУССИАНА
# ==============================================================================
print("\n" + "="*50)
print("ЗАДАНИЕ 1: ДВУМЕРНАЯ ГАУССИАНА")
print("="*50)

def gauss_2d(x, y, A, x0, y0, sigma_x, sigma_y, theta=0, offset=0):
    if theta != 0:
        x_new = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
        y_new = -(x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    else:
        x_new = x - x0
        y_new = y - y0
    exp_part = np.exp(-(x_new ** 2 / (2 * sigma_x ** 2) + y_new ** 2 / (2 * sigma_y ** 2)))
    return A * exp_part + offset

loss_history_gauss = []

def loss_function_gauss(model_params):
    A, x0, y0, sigma_x, sigma_y, theta, offset = model_params
    if sigma_x <= 0 or sigma_y <= 0 or A <= 0:
        return 1e10
    predictions = gauss_2d(X, Y, A, x0, y0, sigma_x, sigma_y, theta, offset)
    return 0.5 * np.mean((predictions - Z) ** 2)

max_idx = np.argmax(Z)
params_start_gauss = [Z[max_idx] + 0.1, X[max_idx], Y[max_idx], np.std(X) * 0.5, np.std(Y) * 0.5, 0.0, 0.0]
bounds_gauss = [(0.1, 10.0), (0.0, 6.0), (0.0, 6.0), (0.1, 5.0), (0.1, 5.0), (-np.pi / 4, np.pi / 4), (-1.0, 1.0)]

loss_history_gauss.append(loss_function_gauss(params_start_gauss))
result_gauss = minimize(loss_function_gauss, params_start_gauss, method='L-BFGS-B', bounds=bounds_gauss,
                        callback=lambda x: loss_history_gauss.append(loss_function_gauss(x)))
A_g, x0_g, y0_g, sx_g, sy_g, theta_g, offset_g = result_gauss.x

print("\nОптимальные параметры (Гауссиана):")
print(f"A = {A_g:.4f}, x0 = {x0_g:.4f}, y0 = {y0_g:.4f}")
print(f"sigma_x = {sx_g:.4f}, sigma_y = {sy_g:.4f}, theta = {theta_g:.4f}, offset = {offset_g:.4f}")
print(f"Финальная MSE: {result_gauss.fun:.8f}")

# ДОБАВЛЕННЫЙ ВЫВОД ДЛЯ ГАУССИАНЫ
print("\nАналитический вид модели (Гауссиана):")
print(f"z(x,y) = {A_g:.4f} * exp(-(x'^2 / (2*{sx_g:.4f}^2) + y'^2 / (2*{sy_g:.4f}^2))) + {offset_g:.4f}")
print(f"где x' = (x - {x0_g:.4f})*cos({theta_g:.4f}) + (y - {y0_g:.4f})*sin({theta_g:.4f})")
print(f"    y' = -(x - {x0_g:.4f})*sin({theta_g:.4f}) + (y - {y0_g:.4f})*cos({theta_g:.4f})")

print("\nНевязки (Гауссиана):")
pred_gauss = gauss_2d(X, Y, A_g, x0_g, y0_g, sx_g, sy_g, theta_g, offset_g)
for i in range(len(X)):
    print(f"Точка {i}: Z_реал = {Z[i]:.2f} | Z_пред = {pred_gauss[i]:.4f} | Невязка = {pred_gauss[i] - Z[i]:.4f}")


# ==============================================================================
# ЗАДАНИЕ 2: ЭЛЛИПТИЧЕСКИЙ ПАРАБОЛОИД
# ==============================================================================
print("\n" + "="*50)
print("ЗАДАНИЕ 2: ЭЛЛИПТИЧЕСКИЙ ПАРАБОЛОИД")
print("="*50)

def paraboloid_2d(x, y, x0, y0, z0, a, b, c):
    return a*(x - x0)**2 + b*(y - y0)**2 + c*(x - x0)*(y - y0) + z0

loss_history_parab = []

def loss_function_parab(params):
    x0, y0, z0, a, b, c = params
    predictions = paraboloid_2d(X, Y, x0, y0, z0, a, b, c)
    return 0.5 * np.mean((predictions - Z) ** 2)

params_start_parab = [X[max_idx], Y[max_idx], Z[max_idx], -1.0, -1.0, 0.0]
bounds_parab = [(0.0, 6.0), (0.0, 6.0), (0.0, 10.0), (-10.0, -0.01), (-10.0, -0.01), (-5.0, 5.0)]

loss_history_parab.append(loss_function_parab(params_start_parab))
result_parab = minimize(loss_function_parab, params_start_parab, method='L-BFGS-B', bounds=bounds_parab,
                        callback=lambda x: loss_history_parab.append(loss_function_parab(x)))
x0_p, y0_p, z0_p, a_p, b_p, c_p = result_parab.x

print("\nОптимальные параметры (Параболоид):")
print(f"x0 = {x0_p:.4f}, y0 = {y0_p:.4f}, z0 = {z0_p:.4f}")
print(f"a = {a_p:.4f}, b = {b_p:.4f}, c = {c_p:.4f}")
print(f"Финальная MSE: {result_parab.fun:.8f}")

# ДОБАВЛЕННЫЙ ВЫВОД ДЛЯ ПАРАБОЛОИДА
print("\nАналитический вид модели (Параболоид):")
print(f"z(x,y) = {a_p:.4f}*(x - {x0_p:.4f})^2 + {b_p:.4f}*(y - {y0_p:.4f})^2 + {c_p:.4f}*(x - {x0_p:.4f})*(y - {y0_p:.4f}) + {z0_p:.4f}")

print("\nНевязки (Параболоид):")
pred_parab = paraboloid_2d(X, Y, x0_p, y0_p, z0_p, a_p, b_p, c_p)
for i in range(len(X)):
    print(f"Точка {i}: Z_реал = {Z[i]:.2f} | Z_пред = {pred_parab[i]:.4f} | Невязка = {pred_parab[i] - Z[i]:.4f}")


# ==============================================================================
# ЗАДАНИЕ 5: RBF-СЕТЬ
# ==============================================================================
print("\n" + "="*50)
print("ЗАДАНИЕ 5: RBF-СЕТЬ")
print("="*50)

def rbf_network(x, y, c1x, c1y, c2x, c2y, s1, s2, w0, w1, w2):
    q1 = ((x - c1x)**2 + (y - c1y)**2) / (2 * s1**2)
    q2 = ((x - c2x)**2 + (y - c2y)**2) / (2 * s2**2)
    return w1 * np.exp(-q1) + w2 * np.exp(-q2) + w0

loss_history_rbf = []

def loss_function_rbf(params):
    c1x, c1y, c2x, c2y, s1, s2, w0, w1, w2 = params
    predictions = rbf_network(X, Y, c1x, c1y, c2x, c2y, s1, s2, w0, w1, w2)
    return 0.5 * np.mean((predictions - Z) ** 2)

c1x_0, c1y_0 = np.mean(X[:2]), np.mean(Y[:2])
c2x_0, c2y_0 = np.mean(X[2:]), np.mean(Y[2:])
dist = np.sqrt((c1x_0 - c2x_0)**2 + (c1y_0 - c2y_0)**2)
s1_0 = s2_0 = dist / 2.0
w0_0, w1_0, w2_0 = 0.0, 1.0, 1.0

params_start_rbf = [c1x_0, c1y_0, c2x_0, c2y_0, s1_0, s2_0, w0_0, w1_0, w2_0]
bounds_rbf = [
    (0.0, 6.0), (0.0, 6.0),  # c1
    (0.0, 6.0), (0.0, 6.0),  # c2
    (0.1, 5.0), (0.1, 5.0),  # sigma 1, 2
    (-10.0, 10.0), (-10.0, 10.0), (-10.0, 10.0) # веса
]

loss_history_rbf.append(loss_function_rbf(params_start_rbf))
result_rbf = minimize(loss_function_rbf, params_start_rbf, method='L-BFGS-B', bounds=bounds_rbf,
                      callback=lambda x: loss_history_rbf.append(loss_function_rbf(x)))
c1x_r, c1y_r, c2x_r, c2y_r, s1_r, s2_r, w0_r, w1_r, w2_r = result_rbf.x

print("\nОптимальные параметры (RBF-сеть):")
print(f"Центр 1: ({c1x_r:.4f}, {c1y_r:.4f}), Ширина 1: {s1_r:.4f}, Вес w1: {w1_r:.4f}")
print(f"Центр 2: ({c2x_r:.4f}, {c2y_r:.4f}), Ширина 2: {s2_r:.4f}, Вес w2: {w2_r:.4f}")
print(f"Смещение w0: {w0_r:.4f}")
print(f"Финальная MSE: {result_rbf.fun:.8f}")

print("\nАналитический вид модели (RBF):")
print(f"z(x,y) = {w1_r:.4f} * exp(-((x - {c1x_r:.4f})^2 + (y - {c1y_r:.4f})^2) / (2*{s1_r:.4f}^2)) +")
print(f"         {w2_r:.4f} * exp(-((x - {c2x_r:.4f})^2 + (y - {c2y_r:.4f})^2) / (2*{s2_r:.4f}^2)) + {w0_r:.4f}")

print("\nНевязки (RBF-сеть):")
pred_rbf = rbf_network(X, Y, c1x_r, c1y_r, c2x_r, c2y_r, s1_r, s2_r, w0_r, w1_r, w2_r)
for i in range(len(X)):
    print(f"Точка {i}: Z_реал = {Z[i]:.2f} | Z_пред = {pred_rbf[i]:.4f} | Невязка = {pred_rbf[i] - Z[i]:.4f}")

# ==============================================================================
# ВИЗУАЛИЗАЦИЯ
# ==============================================================================
x_grid = np.linspace(0, 6, 50)
y_grid = np.linspace(0, 6, 50)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

Z_grid_gauss = gauss_2d(X_grid, Y_grid, A_g, x0_g, y0_g, sx_g, sy_g, theta_g, offset_g)
Z_grid_parab = paraboloid_2d(X_grid, Y_grid, x0_p, y0_p, z0_p, a_p, b_p, c_p)
Z_grid_rbf = rbf_network(X_grid, Y_grid, c1x_r, c1y_r, c2x_r, c2y_r, s1_r, s2_r, w0_r, w1_r, w2_r)

fig = plt.figure(figsize=(18, 15))

def plot_model(row, title, Z_grid, loss_hist, cmap_name):
    ax_3d = fig.add_subplot(3, 3, row*3 - 2, projection='3d')
    ax_3d.plot_surface(X_grid, Y_grid, Z_grid, cmap=cmap_name, alpha=0.7, zorder=1)
    ax_3d.scatter(X, Y, Z, c='red', s=80, edgecolors='black', depthshade=False, zorder=10)
    ax_3d.set_title(f'{title} (3D)')
    ax_3d.set_xlabel('X'); ax_3d.set_ylabel('Y'); ax_3d.set_zlabel('Z')
    # ax_3d.set_zlim(-1, 5)
    ax_3d.view_init(elev=25, azim=45)

    ax_cont = fig.add_subplot(3, 3, row*3 - 1)
    contour = ax_cont.contourf(X_grid, Y_grid, Z_grid, levels=25, cmap=cmap_name, alpha=0.9)
    ax_cont.scatter(X, Y, c=Z, s=100, edgecolors='white', cmap=cmap_name)
    ax_cont.contour(X_grid, Y_grid, Z_grid, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    ax_cont.set_title(f'{title} (Линии уровня)')
    plt.colorbar(contour, ax=ax_cont)

    ax_loss = fig.add_subplot(3, 3, row*3)
    ax_loss.plot(range(len(loss_hist)), loss_hist, marker='o', color='black', linewidth=2)
    ax_loss.set_title(f'Обучение (MSE)')
    ax_loss.set_xlabel('Итерации')
    ax_loss.grid(True, linestyle='--', alpha=0.6)

plot_model(1, 'Гауссиана', Z_grid_gauss, loss_history_gauss, 'viridis')
plot_model(2, 'Параболоид', Z_grid_parab, loss_history_parab, 'plasma')
plot_model(3, 'RBF-сеть', Z_grid_rbf, loss_history_rbf, 'magma')

plt.tight_layout()
plt.savefig('all_models_results.png', dpi=300)
plt.show()