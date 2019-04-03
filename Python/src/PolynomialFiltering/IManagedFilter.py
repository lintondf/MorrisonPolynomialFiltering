'''
Created on Mar 13, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod

from enum import Enum
from numpy import array, eye, zeros, isscalar
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilterWithCovariance


class IObservationErrorModel(ABC):
    def __init__(self):
        pass

    @abstractmethod # pragma: no cover
    def getInverseCovariance(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int) -> array:
        pass
    

    
    
class IManagedFilter(ABC):
    def __init__(self,name : str = ''):
        super().__init__(name);
    
    @abstractmethod # pragma: no cover 
    def getGoodnessOfFit(self) -> float:
        pass
    
    @abstractmethod # pragma: no cover
    def add(self, t : float, y : vector, observationId : int = 0) -> None:    
        pass

    @abstractmethod # pragma: no cover
    def setObservationInverseR(self, inverseR:array):
        pass
        
    @abstractmethod # pragma: no cover  
    def setObservationErrorModel(self, errorModel : IObservationErrorModel):
        pass

    
if __name__ == '__main__':
    pass