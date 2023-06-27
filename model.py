import pyscipopt as scip
class Planning:
    """
    模型参考：1.5.1: 调合计划问题模型
    """
    def __init__(self,data):
        self.data = data
        I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price = self._preprocessing()


    def _preprocessing(self):
        """
        :return:
            I: 组分的下标集合
            J: 产品的下标集合
            K: 物性的下标集合
            Q: 组分i的物性k的数据
            P: 产品j物性k的控制规格
            LX: 组分i可供使用的下限
            UX: 组分i可供使用的上限
            LY: 产品j调合量的下限
            UY: 产品j调合量的上限
            C: 组分i的单位成本价格
            Price: 产品j的单位销售价格
        """
        I,J,K = self.data["components"],self.data[""]
        return I, J, K, Q, Pmin, Pmax, LX, UX, LY, UY, C, Price
