'''
Created on Feb 19, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import Tuple

from numpy import array

from PolynomialFiltering.Main import AbstractFilter

class IRecursiveFilter(AbstractFilter):
    def __init__(self):
        pass
    

    @abstractmethod   
    def start(self, t : float, Z : array) -> None:
        raise NotImplementedError()
        
    @abstractmethod   
    def predict(self, t : float) -> Tuple[array, array, array] :
        raise NotImplementedError()
 
    @abstractmethod   
    def update(self, t : float, dtau : array, Zstar : array, e : array) -> None:
        raise NotImplementedError()
       
    @abstractmethod   
    def getN(self)->int:
        raise NotImplementedError()
    
    @abstractmethod   
    def getTime(self) -> array:
        raise NotImplementedError()
    
    @abstractmethod   
    def getState(self, t : float) -> array:
        raise NotImplementedError()
