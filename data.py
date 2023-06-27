from dataclasses import dataclass
from typing import List, Dict, Union


@dataclass
class RefineryData:
    """
    Data class for optimization data in crude oil refining.
    """
    I: List[Union[str, int]]  # Set of indices for components
    J: List[Union[str, int]]  # Set of indices for products
    K: List[Union[str, int]]  # Set of indices for properties
    Q: Dict[Union[str, int], Dict[Union[str, int], float]]  # Data for property k of component i
    Pmin: Dict[Union[str, int], Dict[Union[str, int], float]]  # Control specification for property k of product j
    Pmax: Dict[Union[str, int], Dict[Union[str, int], float]]  # Control specification for property k of product j
    LX: Dict[Union[str, int], float]  # Lower limit of component i available for use
    UX: Dict[Union[str, int], float]  # Upper limit of component i available for use
    LY: Dict[Union[str, int], float]  # Lower limit of blending quantity for product j
    UY: Dict[Union[str, int], float]  # Upper limit of blending quantity for product j
    C: Dict[Union[str, int], float]  # Unit cost price of component i
    Price: Dict[Union[str, int], float]  # Unit selling price of product j


ex_data = RefineryData(I=["CM1", "CM2", "CM3", "CM4", "CM5", "CM6"],  # 6种组分
                       J=["G90", "G93", "G97"],  # 3种汽油
                       K=["SUL", "RON", "DON", "ARW", "OLE"],  # 5种物性
                       Price={"G90": 3140, "G93": 3328, "G97": 3517},
                       C={"CM1": 2356.3, "CM2": 2396.1, "CM3": 2347.2, "CM4": 2470.8, "CM5": 2513.8, "CM6": 3500},
                       LX={"CM1": 2.835, "CM2": 2.205, "CM3": 4.305, "CM4": 0, "CM5": 0, "CM6": 0},
                       UX={"CM1": 2.835, "CM2": 2.205, "CM3": 4.305, "CM4": 0.9, "CM5": 5.4, "CM6": 0.45},
                       LY={"G90": 8, "G93": 6, "G97": 1},
                       UY={"G90": 1000, "G93": 1000, "G97": 1000},
                       Q={("CM1", "SUL"): 0.04, ("CM1", "RON"): 89.5, ("CM1", "DON"): 84.25, ("CM1", "ARW"): 12.7,
                          ("CM1", "OLE"): 39.2,
                          ("CM2", "SUL"): 0.04, ("CM2", "RON"): 93.2, ("CM2", "DON"): 87.1, ("CM2", "ARW"): 21.4,
                          ("CM2", "OLE"): 32.4,
                          ("CM3", "SUL"): 0.04, ("CM3", "RON"): 89.8, ("CM3", "DON"): 84.9, ("CM3", "ARW"): 13,
                          ("CM3", "OLE"): 39,
                          ("CM4", "SUL"): 0.001, ("CM4", "RON"): 54.8, ("CM4", "DON"): 50, ("CM4", "ARW"): 0.05,
                          ("CM4", "OLE"): 0,
                          ("CM5", "SUL"): 0.001, ("CM5", "RON"): 98.5, ("CM5", "DON"): 93, ("CM5", "ARW"): 70,
                          ("CM5", "OLE"): 0,
                          ("CM6", "SUL"): 0.001, ("CM6", "RON"): 114, ("CM6", "DON"): 107, ("CM6", "ARW"): 0,
                          ("CM6", "OLE"): 0},
                       Pmin={("G90", "SUL"): 0, ("G90", "RON"): 90.1, ("G90", "DON"): 85.1, ("G90", "OLE"): 0,
                             ("G90", "ARW"): 0,
                             ("G93", "SUL"): 0, ("G93", "RON"): 93.1, ("G93", "DON"): 88.1, ("G93", "OLE"): 0,
                             ("G93", "ARW"): 0,
                             ("G97", "SUL"): 0, ("G97", "RON"): 97.1, ("G97", "DON"): 92.1, ("G97", "OLE"): 0,
                             ("G97", "ARW"): 0},
                       Pmax={("G90", "SUL"): 0.07, ("G90", "RON"): 999, ("G90", "DON"): 999, ("G90", "OLE"): 34,
                             ("G90", "ARW"): 40,
                             ("G93", "SUL"): 0.07, ("G93", "RON"): 999, ("G93", "DON"): 999, ("G93", "OLE"): 34,
                             ("G93", "ARW"): 40,
                             ("G97", "SUL"): 0.07, ("G97", "RON"): 999, ("G97", "DON"): 999, ("G97", "OLE"): 34,
                             ("G97", "ARW"): 40})
