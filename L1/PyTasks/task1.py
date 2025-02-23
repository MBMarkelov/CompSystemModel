import numpy as np
import pulp
import cvxpy as cp

def minimaize_solution():
    # Данные задачи
    lengths = np.array([45, 35, 50])  # Длины заготовок
    required_pieces = np.array([40, 30, 20])  # Требуемое количество
    bar_length = 110  # Длина прута
    cut_patterns = np.array([
        [2, 0, 0],
        [1, 1, 0],
        [1, 0, 1],
        [0, 3, 0],
        [0, 1, 1],
        [0, 0, 2]
    ])

    #pulp
    prob_pulp = pulp.LpProblem("CuttingStock", pulp.LpMinimize)
    x_pulp = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(len(cut_patterns))]
    prob_pulp += pulp.lpSum(x_pulp)  # Минимизируем количество прутьев
    for j in range(len(lengths)):
        prob_pulp += pulp.lpSum(cut_patterns[i, j] * x_pulp[i] for i in range(len(cut_patterns))) >= required_pieces[j]
    prob_pulp.solve()
    pulp_result = [pulp.value(var) for var in x_pulp]

    # Выпуклое программирование (cvxpy)
    x_cvxpy = cp.Variable(len(cut_patterns), integer=True)
    constraints = [x_cvxpy >= 0]
    for j in range(len(lengths)):
        constraints.append(cut_patterns[:, j] @ x_cvxpy >= required_pieces[j])
    objective = cp.Minimize(cp.sum(x_cvxpy))
    prob_cvxpy = cp.Problem(objective, constraints)
    prob_cvxpy.solve()
    cvxpy_result = x_cvxpy.value


    # Вывод результатов
    print("Pulp result:", pulp_result)
    print("CVXPY result:", cvxpy_result)

if __name__ == "__main__":
    print("f")
    minimaize_solution()