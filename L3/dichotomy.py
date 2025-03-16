import math
import numpy as np
import matplotlib.pyplot as plt
from L3.Function import f
from io import BytesIO
import base64

def dichotomy_method(f, a, b, tol=1e-6):
    while abs(b - a) > tol:
        midpoint = (a + b) / 2
        left = midpoint - tol / 2
        right = midpoint + tol / 2

        if f(left) < f(right):
            b = right
        else:
            a = left

    return (a + b) / 2


def dichotomy_selection():
    a, b = -20, 20
    x_min = dichotomy_method(f, a, b)
    y_min = f(x_min)

    x_max = dichotomy_method(lambda x: -f(x), a, b)
    y_max = f(x_max)

    x = np.linspace(-100, 100, 500)
    x_filtered = [x_i for x_i in x if abs(1 + np.sin(x_i)) > 1e-3]
    y = [f(x_i) for x_i in x_filtered]

    plt.figure(figsize=(10, 6))
    plt.plot(x_filtered, y, 'b-', label='f(x)')
    plt.plot(x_min, y_min, 'go', label="Локальный минимум")
    plt.plot(x_max, y_max, 'ro', label="Локальный максимум")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.xlim(-25, 50)
    plt.ylim(-10, 25)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    lower_bound = 3 * math.pi / 2
    upper_bound = 7 * math.pi / 2

    extrema_data = {
        "min": {"x": round(x_min, 4), "y": round(y_min, 4)},
        "max": {"x": round(x_max, 4), "y": round(y_max, 4)},
        "extrema_interval": f"({round(lower_bound, 4)} + 2pin, {round(upper_bound, 4)} + 2pin), n - целое число",
        "image": img_base64
    }

    return extrema_data
