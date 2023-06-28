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
