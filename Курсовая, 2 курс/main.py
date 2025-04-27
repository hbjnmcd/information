from scipy.optimize import linprog

c = [-1, -1, -1, -1]
A = [[3, 2, 1, 0], [1, 6, 9, 13]]
b = [80, 40]
x1 = (0,None)
x2 = (0,None)
x3 = (0,None)
x4 = (0,None)
res = linprog(c,A_ub=A,b_ub=b,bounds=(x1,x2,x3,x4),method='simplex')

print("Оптимальное решение:", res.x)
print("Оптимальное значение целевой функции:", -res.fun)

from ortools.linear_solver import pywraplp
def solve_linear_programming():
    solver = pywraplp.Solver.CreateSolver('GLOP')

    x1 = solver.NumVar(0, solver.infinity(), 'x1')
    x2 = solver.NumVar(0, solver.infinity(), 'x2')
    x3 = solver.NumVar(0, solver.infinity(), 'x3')
    x4 = solver.NumVar(0, solver.infinity(), 'x4')

    # Устанавливаем целевую функцию
    objective = solver.Objective()
    objective.SetCoefficient(x1, 1)
    objective.SetCoefficient(x2, 1)
    objective.SetCoefficient(x3, 1)
    objective.SetCoefficient(x4, 1)
    objective.SetMinimization()

    # Добавляем ограничения
    constraint1 = solver.Constraint(80, solver.infinity())
    constraint1.SetCoefficient(x1, 3)
    constraint1.SetCoefficient(x2, 2)
    constraint1.SetCoefficient(x3, 1)
    constraint1.SetCoefficient(x4, 0)

    constraint2 = solver.Constraint(40, solver.infinity())
    constraint2.SetCoefficient(x1, 1)
    constraint2.SetCoefficient(x2, 6)
    constraint2.SetCoefficient(x3, 9)
    constraint2.SetCoefficient(x4, 13)

    solver.Solve()

    if solver.Solve() == solver.OPTIMAL:
        print('Решение:')
        print('x1 = ', x1.solution_value())
        print('x2 = ', x2.solution_value())
        print('x3 = ', x3.solution_value())
        print('x4 = ', x4.solution_value())
        print('Значение целевой функции: ', objective.Value())
    else:
        print('Решение не обнаружено.')

solve_linear_programming()

