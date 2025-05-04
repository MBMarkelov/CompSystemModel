import math

def erlang_b(c, a):
    """Формула Эрланга B — вероятность отказа"""
    numerator = (a ** c) / math.factorial(c)
    denominator = sum((a ** k) / math.factorial(k) for k in range(c + 1))
    return numerator / denominator

lambda_min, lambda_max = 0.7, 0.9
T_min, T_max = 2.3, 2.5

λ = lambda_max
T = T_max
μ = 1 / T
a = λ / μ  

# Подбор минимального количества каналов при B(c, a) < 0.1
for c in range(1, 100):
    B = erlang_b(c, a)
    if B < 0.1:
        print(f"Минимальное количество каналов: {c}")
        print(f"Вероятность отказа: {B:.4f}")
        break
