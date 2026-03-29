import numpy as np

def f1(x): return x**3 - 3.125*x**2 - 3.5*x + 2.458
def f2(x): return np.sin(x) + 0.1 * x**2 - 1
def f3(x): return np.exp(x) - 2 * x - 2

EQUATIONS = {
    1: {"func": f1, "str": "x^3 - 3.125x^2 - 3.5x + 2.458 = 0"},
    2: {"func": f2, "str": "sin(x) + 0.1x^2 - 1 = 0"},
    3: {"func": f3, "str": "e^x - 2x - 2 = 0"}
}

def sys1_f1(x, y): return np.sin(x + 0.5) - y - 1
def sys1_f2(x, y): return np.cos(y - 2) + x
def sys1_df1dx(x, y): return np.cos(x + 0.5)
def sys1_df1dy(x, y): return -1.0
def sys1_df2dx(x, y): return 1.0
def sys1_df2dy(x, y): return -np.sin(y - 2)

def sys2_f1(x, y): return x**2 + y**2 - 4
def sys2_f2(x, y): return -3*x**2 + y
def sys2_df1dx(x, y): return 2*x
def sys2_df1dy(x, y): return 2*y
def sys2_df2dx(x, y): return -6*x
def sys2_df2dy(x, y): return 1.0

SYSTEMS = {
    1: {
        "str": "1) sin(x+0.5) - y = 1\n   2) cos(y-2) + x = 0",
        "f1": sys1_f1, "f2": sys1_f2,
        "df1dx": sys1_df1dx, "df1dy": sys1_df1dy,
        "df2dx": sys1_df2dx, "df2dy": sys1_df2dy
    },
    2: {
        "str": "1) x^2 + y^2 = 4\n   2) y = 3x^2",
        "f1": sys2_f1, "f2": sys2_f2,
        "df1dx": sys2_df1dx, "df1dy": sys2_df1dy,
        "df2dx": sys2_df2dx, "df2dy": sys2_df2dy
    }
}