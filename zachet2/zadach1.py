import pulp

model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

x1 = pulp.LpVariable("Caramel_Type_1", lowBound=0)
x2 = pulp.LpVariable("Caramel_Type_2", lowBound=0)

model += 1080 * x1 + 1120 * x2, "Profit"

model += 0.5 * x1 + 0.8 * x2 <= 80    # сахар
model += 0.4 * x1 + 0.3 * x2 <= 60    # патока
model += 0.1 * x1 + 0.1 * x2 <= 13    # пюре

model.solve()

print(f"Произвести карамели 1 вида: {x1.varValue:.2f} т")
print(f"Произвести карамели 2 вида: {x2.varValue:.2f} т")
print(f"Максимальная прибыль: {pulp.value(model.objective):.2f} у.е.")
