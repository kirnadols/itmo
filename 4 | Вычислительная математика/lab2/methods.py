import numpy as np


def derivative(f, x, dx=1e-5):
    return (f(x + dx) - f(x - dx)) / (2 * dx)


def second_derivative(f, x, dx=1e-5):
    return (f(x + dx) - 2 * f(x) + f(x - dx)) / (dx ** 2)


def verify_interval(f, a, b):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    sign_changes = np.sum(np.diff(np.sign(y_vals)) != 0)

    if sign_changes == 0:
        return False, "На заданном интервале корней нет (или функция не пересекает ось X)."
    elif sign_changes > 1:
        return False, f"На заданном интервале несколько корней (смен знака: {sign_changes}). Сузьте интервал."
    return True, "Интервал корректен (один корень)."


def get_initial_approximation(f, a, b):
    if f(a) * second_derivative(f, a) > 0:
        return a, b
    elif f(b) * second_derivative(f, b) > 0:
        return b, a
    return a, b


def chord_method(f, a, b, eps, max_iter=1000):
    x_fixed, x_curr = get_initial_approximation(f, a, b)
    history = []

    for i in range(max_iter):
        x_next = x_curr - f(x_curr) * (x_fixed - x_curr) / (f(x_fixed) - f(x_curr))
        diff = abs(x_next - x_curr)
        history.append((i + 1, x_next, f(x_next), diff))

        if diff <= eps or abs(f(x_next)) <= eps:
            return x_next, history
        x_curr = x_next
    return x_curr, history


def secant_method(f, a, b, eps, max_iter=1000):
    x0, _ = get_initial_approximation(f, a, b)
    x1 = x0 + eps if x0 == a else x0 - eps
    history = []

    for i in range(max_iter):
        if f(x1) - f(x0) == 0: break
        x_next = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        diff = abs(x_next - x1)
        history.append((i + 1, x_next, f(x_next), diff))

        if diff <= eps or abs(f(x_next)) <= eps:
            return x_next, history
        x0, x1 = x1, x_next
    return x1, history


def simple_iteration_method(f, a, b, eps, max_iter=1000):
    x_vals = np.linspace(a, b, 100)
    f_primes = [derivative(f, x) for x in x_vals]
    max_df = max(abs(min(f_primes)), abs(max(f_primes)))

    if min(f_primes) > 0:
        lam = -1 / max_df
    else:
        lam = 1 / max_df

    def phi(x):
        return x + lam * f(x)

    def phi_prime(x):
        return 1 + lam * derivative(f, x)

    q = max([abs(phi_prime(x)) for x in x_vals])
    q_status = f"Коэффициент сжатия q = {q:.5f}. "
    if q >= 1:
        q_status += "Условие сходимости НЕ выполняется!"
    else:
        q_status += "Условие сходимости выполняется."

    x_curr, _ = get_initial_approximation(f, a, b)
    history = []

    for i in range(max_iter):
        x_next = phi(x_curr)
        diff = abs(x_next - x_curr)
        history.append((i + 1, x_curr, x_next, phi(x_next), f(x_next), diff))

        stop_cond = eps if q >= 0.5 else eps * (1 - q) / q
        if diff <= stop_cond or abs(f(x_next)) <= eps:
            return x_next, history, q_status
        x_curr = x_next
    return x_curr, history, q_status


def newton_system(sys, x0, y0, eps, max_iter=100):
    x_curr, y_curr = x0, y0
    history = []

    for i in range(max_iter):
        a11, a12 = sys["df1dx"](x_curr, y_curr), sys["df1dy"](x_curr, y_curr)
        a21, a22 = sys["df2dx"](x_curr, y_curr), sys["df2dy"](x_curr, y_curr)

        b1, b2 = -sys["f1"](x_curr, y_curr), -sys["f2"](x_curr, y_curr)

        det = a11 * a22 - a12 * a21
        if det == 0: break

        dx = (b1 * a22 - a12 * b2) / det
        dy = (a11 * b2 - b1 * a21) / det

        x_next, y_next = x_curr + dx, y_curr + dy
        history.append((i + 1, x_next, y_next, abs(dx), abs(dy)))

        if max(abs(dx), abs(dy)) <= eps:
            return (x_next, y_next), history
        x_curr, y_curr = x_next, y_next

    return (x_curr, y_curr), history