"""
模型参考：1.5.1: 调合计划问题模型
"""
import pyscipopt as scip
import pandas as pd
import pulp


def create_model(I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price):
    """
    :param I: 组分的下标集合
    :param J: 产品的下标集合
    :param K: 物性的下标集合
    :param Q: 组分i的物性k的数据
    :param P: 产品j物性k的控制规格
    :param LX: 组分i可供使用的下限
    :param UX: 组分i可供使用的上限
    :param LY: 产品j调合量的下限
    :param UY: 产品j调合量的上限
    :param C: 组分i的单位成本价格
    :param Price: 产品j的单位销售价格
    :return:
    """
    model = scip.Model()
    x, y, b = {}, {}, {}
    for i in I:
        x[i] = model.addVar(name=f"x_{i}", lb=LX[i], ub=UX[i])
    for j in J:
        y[j] = model.addVar(name=f"y_{j}", lb=LY[j], ub=UY[j])
    for i in I:
        for j in J:
            b[i, j] = model.addVar(name=f"b_{i}_{j}")

    for i in I:
        model.addCons(scip.quicksum(b[i, j] for j in J) == x[i])

    for j in J:
        model.addCons(scip.quicksum(b[i, j] for i in I) == y[j])

    for j in J:
        for k in K:
            model.addCons(scip.quicksum(Q[(i, k)] * b[i, j] for i in I) <= Pmax[(j, k)] * y[j])
            model.addCons(scip.quicksum(Q[(i, k)] * b[i, j] for i in I) >= Pmin[(j, k)] * y[j])

    # obj
    obj = scip.quicksum(-C[i] * x[i] for i in I) + scip.quicksum(Price[j] * y[j] for j in J)
    model.setObjective(obj, "maximize")
    model.optimize()
    # 解的处理
    solution = pd.DataFrame(columns=J, index=I)
    for i in I:
        for j in J:
            solution.loc[i, j] = model.getVal(b[i, j])
    result = pd.DataFrame(columns=J, index=K)
    for k in K:
        for j in J:
            result.loc[k, j] = sum([Q[(i, k)] * model.getVal(b[i, j]) for i in I]) / model.getVal(y[j])
    model.writeProblem("ex.mps")
    print(solution)
    print(result)
    return model


# def create_model(I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price):
#     """
#     :param I: 组分的下标集合
#     :param J: 产品的下标集合
#     :param K: 物性的下标集合
#     :param Q: 组分i的物性k的数据
#     :param P: 产品j物性k的控制规格
#     :param LX: 组分i可供使用的下限
#     :param UX: 组分i可供使用的上限
#     :param LY: 产品j调合量的下限
#     :param UY: 产品j调合量的上限
#     :param C: 组分i的单位成本价格
#     :param Price: 产品j的单位销售价格
#     :return:
#     """
#     model = pulp.LpProblem("Production Planning", pulp.LpMaximize)
#     x = pulp.LpVariable.dicts("x", I, lowBound=0, cat='Continuous')
#     y = pulp.LpVariable.dicts("y", J, lowBound=0, cat='Continuous')
#     b = pulp.LpVariable.dicts("b", (I, J), lowBound=0, cat='Continuous')
#     for i in I:
#         x[i].bounds(LX[i], UX[i])
#
#     for j in J:
#         y[j].bounds(LY[j], UY[j])
#
#     for i in I:
#         model += pulp.lpSum(b[i][j] for j in J) == x[i]
#
#     for j in J:
#         model += pulp.lpSum(b[i][j] for i in I) == y[j]
#
#     for j in J:
#         for k in K:
#             model += pulp.lpSum(Q[(i, k)] * b[i][j] for i in I) <= Pmax[(j, k)] * y[j]
#             model += pulp.lpSum(Q[(i, k)] * b[i][j] for i in I) >= Pmin[(j, k)] * y[j]
#
#     # obj
#     obj = pulp.lpSum(-C[i] * x[i] for i in I) + pulp.lpSum(Price[j] * y[j] for j in J)
#     model.setObjective(obj)
#
#     model.solve()
#     solution = pd.DataFrame(columns=["G90", "G93", "G97"], index=["CM1", "CM2", "CM3", "CM4", "CM5", "CM6"])
#     for i in I:
#         for j in J:
#             solution.loc[i, j] = b[i][j].value()
#     print(solution)
#     return solution


def example():
    I = ["CM1", "CM2", "CM3", "CM4", "CM5", "CM6"]  # 6种组分
    J = ["G90", "G93", "G97"]  # 3种汽油
    K = ["SUL", "RON", "DON", "ARW", "OLE"]  # 5种物性
    Price = {"G90": 3140, "G93": 3328, "G97": 3517}
    C = {"CM1": 2356.3, "CM2": 2396.1, "CM3": 2347.2, "CM4": 2470.8, "CM5": 2513.8, "CM6": 3500}
    LX = {"CM1": 2.835, "CM2": 2.205, "CM3": 4.305, "CM4": 0, "CM5": 0, "CM6": 0}
    UX = {"CM1": 2.835, "CM2": 2.205, "CM3": 4.305, "CM4": 0.9, "CM5": 5.4, "CM6": 0.45}
    LY = {"G90": 8, "G93": 6, "G97": 1}
    UY = {"G90": 1000, "G93": 1000, "G97": 1000}
    Q = {("CM1", "SUL"): 0.04, ("CM1", "RON"): 89.5, ("CM1", "DON"): 84.25, ("CM1", "ARW"): 12.7, ("CM1", "OLE"): 39.2,
         ("CM2", "SUL"): 0.04, ("CM2", "RON"): 93.2, ("CM2", "DON"): 87.1, ("CM2", "ARW"): 21.4, ("CM2", "OLE"): 32.4,
         ("CM3", "SUL"): 0.04, ("CM3", "RON"): 89.8, ("CM3", "DON"): 84.9, ("CM3", "ARW"): 13, ("CM3", "OLE"): 39,
         ("CM4", "SUL"): 0.001, ("CM4", "RON"): 54.8, ("CM4", "DON"): 50, ("CM4", "ARW"): 0.05, ("CM4", "OLE"): 0,
         ("CM5", "SUL"): 0.001, ("CM5", "RON"): 98.5, ("CM5", "DON"): 93, ("CM5", "ARW"): 70, ("CM5", "OLE"): 0,
         ("CM6", "SUL"): 0.001, ("CM6", "RON"): 114, ("CM6", "DON"): 107, ("CM6", "ARW"): 0, ("CM6", "OLE"): 0}
    Pmin = {("G90", "SUL"): 0, ("G90", "RON"): 90.1, ("G90", "DON"): 85.1, ("G90", "OLE"): 0, ("G90", "ARW"): 0,
            ("G93", "SUL"): 0, ("G93", "RON"): 93.1, ("G93", "DON"): 88.1, ("G93", "OLE"): 0, ("G93", "ARW"): 0,
            ("G97", "SUL"): 0, ("G97", "RON"): 97.1, ("G97", "DON"): 92.1, ("G97", "OLE"): 0, ("G97", "ARW"): 0}
    Pmax = {("G90", "SUL"): 0.07, ("G90", "RON"): 999, ("G90", "DON"): 999, ("G90", "OLE"): 34, ("G90", "ARW"): 40,
            ("G93", "SUL"): 0.07, ("G93", "RON"): 999, ("G93", "DON"): 999, ("G93", "OLE"): 34, ("G93", "ARW"): 40,
            ("G97", "SUL"): 0.07, ("G97", "RON"): 999, ("G97", "DON"): 999, ("G97", "OLE"): 34, ("G97", "ARW"): 40}
    create_model(I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price)


if __name__ == '__main__':
    example()
