import numpy as np
import pulp
import cvxpy as cp
from scipy.optimize import linprog

def minimize_solution():
    # Исходные данные
    lengths = np.array([45, 35, 50])  # Длины заготовок
    required_pieces = np.array([40, 30, 20])  # Требуемое количество
    bar_length = 110  # Длина прута

    # Варианты разрезки
    cut_patterns = np.array([
        [2, 0, 0],  # x1
        [1, 1, 0],  # x2
        [1, 0, 1],  # x3
        [0, 3, 0],  # x4
        [0, 1, 1],  # x5
        [0, 0, 2]   # x6
    ])

    pattern_lengths = np.sum(cut_patterns * lengths, axis=1)

    assert np.all(pattern_lengths <= bar_length), "Некоторые шаблоны превышают 110 см!"

    ### PuLP (линейное программирование)
    prob_pulp = pulp.LpProblem("CuttingStock", pulp.LpMinimize)

    x_pulp = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(len(cut_patterns))]

    prob_pulp += pulp.lpSum(x_pulp)

    for j in range(len(lengths)):
        prob_pulp += pulp.lpSum(cut_patterns[i, j] * x_pulp[i] for i in range(len(cut_patterns))) >= required_pieces[j]

    prob_pulp.solve()
    pulp_result = [pulp.value(var) for var in x_pulp]

    print("PuLP Result:", pulp_result)

    ### CVXPY
    x_cvxpy = cp.Variable(len(cut_patterns), integer=True)

    constraints = [x_cvxpy >= 0]
    for j in range(len(lengths)):
        constraints.append(cut_patterns[:, j] @ x_cvxpy >= required_pieces[j])

    objective = cp.Minimize(cp.sum(x_cvxpy))
    prob_cvxpy = cp.Problem(objective, constraints)
    prob_cvxpy.solve()

    cvxpy_result = x_cvxpy.value
    print("CVXPY Result:", cvxpy_result)

    ### SciPy
    c = np.ones(len(cut_patterns))
    A_ub = -cut_patterns.T  # Переводим в ≤
    b_ub = -required_pieces  # Изменяем знаки

    bounds = [(0, None)] * len(cut_patterns)

    res_scipy = linprog(c, A_ub=A_ub, b_ub=b_ub, method='highs', bounds=bounds)

    scipy_result = res_scipy.x if res_scipy.success else None
    print("SciPy Result:", scipy_result)

    return pulp_result, cvxpy_result, scipy_result

if __name__ == '__main__':
    minimize_solution()
