import pyscipopt as scip
import pandas as pd
from data import RefineryData, ex_data


class Planning:
    """
    模型参考：1.5.1: 调合计划问题模型
    """

    def __init__(self, data: RefineryData):
        self.data = data
        I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price = self._preprocessing()
        self._create_model(I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price)

    def _preprocessing(self):
        """
        :return:
            I: 组分的下标集合
            J: 产品的下标集合
            K: 物性的下标集合
            Q: 组分i的物性k的数据
            Pmin: 产品j物性k的控制规格下限
            Pmax: 产品j物性k的控制规格上限
            LX: 组分i可供使用的下限
            UX: 组分i可供使用的上限
            LY: 产品j调合量的下限
            UY: 产品j调合量的上限
            C: 组分i的单位成本价格
            Price: 产品j的单位销售价格
        """
        return self.data.I, self.data.J, self.data.K, self.data.Q, \
            self.data.Pmin, self.data.Pmax, self.data.LX, self.data.UX, \
            self.data.LY, self.data.UY, self.data.C, self.data.Price

    def _create_model(self, I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price):
        self.model = scip.Model()
        self.x, self.y, self.b = {}, {}, {}
        for i in I:
            self.x[i] = self.model.addVar(name=f"x_{i}", lb=LX[i], ub=UX[i])
        for j in J:
            self.y[j] = self.model.addVar(name=f"y_{j}", lb=LY[j], ub=UY[j])
        for i in I:
            for j in J:
                self.b[i, j] = self.model.addVar(name=f"b_{i}_{j}")

        for i in I:
            self.model.addCons(scip.quicksum(self.b[i, j] for j in J) == self.x[i])

        for j in J:
            self.model.addCons(scip.quicksum(self.b[i, j] for i in I) == self.y[j])

        for j in J:
            for k in K:
                self.model.addCons(scip.quicksum(Q[(i, k)] * self.b[i, j] for i in I) <= Pmax[(j, k)] * self.y[j])
                self.model.addCons(scip.quicksum(Q[(i, k)] * self.b[i, j] for i in I) >= Pmin[(j, k)] * self.y[j])

        # obj
        obj = scip.quicksum(-C[i] * self.x[i] for i in I) + scip.quicksum(Price[j] * self.y[j] for j in J)
        self.model.setObjective(obj, "maximize")

    def solve(self):
        self.model.optimize()
        solution = pd.DataFrame(columns=self.data.J, index=self.data.I)
        for i in self.data.I:
            for j in self.data.J:
                solution.loc[i, j] = self.model.getVal(self.b[i, j])
        result = pd.DataFrame(columns=self.data.J, index=self.data.K)
        for k in self.data.K:
            for j in self.data.J:
                result.loc[k, j] = sum([self.data.Q[(i, k)] * self.model.getVal(self.b[i, j]) for i in self.data.I]) / \
                                   self.model.getVal(self.y[j])
        print(solution)
        print(result)


ex_model = Planning(ex_data)
ex_model.solve()