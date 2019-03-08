'''
Created on Feb 19, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import Tuple

from numpy import array
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilter

class IRecursiveFilter(AbstractFilter):
    def __init__(self):
        pass
    

    @abstractmethod   
    def start(self, t : float, Z : vector) -> None:
        pass
        
    """ predict - predict state at time t
        
    Parameters
    ----------
    t : float
        time for estimate

    Returns
    -------
    Tuple[array, float, float]
        predicted state at t
        delta t
        delta tau
    """
    @abstractmethod   
    def predict(self, t : float) -> vector :
        pass
 
    @abstractmethod   
    def update(self, t : float, Zstar : vector, e : float) -> None:
        pass
       
    @abstractmethod   
    def getN(self)->int:
        pass
    
    @abstractmethod   
    def getTime(self) -> float:
        pass
    
    @abstractmethod   
    def getState(self, t : float) -> vector:
        pass
