import math
import numpy as np
from scipy.optimize import golden
import matplotlib.pyplot as plt
from L3.Function import f
from io import BytesIO
import base64

def golden_section_math(f, a, b, tol=1e-6):
    phi = (1 + math.sqrt(5)) / 2

    while b - a > tol:
        c = a + (b - a) * (3 - math.sqrt(5)) / 2
        d = a + (b - a) * (math.sqrt(5) - 1) / 2

        if f(c) < f(d):
            b = d
        else:
            a = c

    return (a + b) / 2

def golden_selection_scipy():
    a, b = -1, 1
    x_min = golden(f, brack=(a, b))
    y_min = f(x_min)

    x_max = golden(lambda x: -f(x), brack=(a, b))
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
    plt.xlim(-10, 10)
    plt.ylim(-10, 25)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    extrema_x = np.linspace(-20, 20, 1000)
    extrema_y = np.gradient([f(x) for x in extrema_x])
    extrema_points = [extrema_x[i] for i in range(1, len(extrema_y) - 1) if extrema_y[i-1] * extrema_y[i] < 0]
    
    extrema_data = {
        "min": {"x": round(x_min, 4), "y": round(y_min, 4)},
        "max": {"x": round(x_max, 4), "y": round(y_max, 4)},
        "extrema_points": [round(x, 4) for x in extrema_points],
        "image": img_base64
    }

    return extrema_data


def golden_selection_manual():
    a = -20
    b = 20
    x_min = golden_section_math(f, a, b)
    y_min = f(x_min)

    x_max = golden_section_math(lambda x: -f(x), a, b)
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

    extrema_x = np.linspace(-20, 20, 1000)
    extrema_y = np.gradient([f(x) for x in extrema_x])
    extrema_points = [extrema_x[i] for i in range(1, len(extrema_y) - 1) if extrema_y[i-1] * extrema_y[i] < 0]
    
    extrema_data = {
        "min": {"x": round(x_min, 4), "y": round(y_min, 4)},
        "max": {"x": round(x_max, 4), "y": round(y_max, 4)},
        "extrema_points": [round(x, 4) for x in extrema_points],
        "image": img_base64
    }

    return extrema_data