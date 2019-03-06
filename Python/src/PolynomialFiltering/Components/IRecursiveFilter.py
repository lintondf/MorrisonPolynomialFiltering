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
        raise NotImplementedError()
        
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
    def predict(self, t : float) -> Tuple[vector, float, float] :
        raise NotImplementedError()
 
    @abstractmethod   
    def update(self, t : float, dtau : float, Zstar : vector, e : vector) -> None:
        raise NotImplementedError()
       
    @abstractmethod   
    def getN(self)->int:
        raise NotImplementedError()
    
    @abstractmethod   
    def getTime(self) -> float:
        raise NotImplementedError()
    
    @abstractmethod   
    def getState(self, t : float) -> vector:
        raise NotImplementedError()
