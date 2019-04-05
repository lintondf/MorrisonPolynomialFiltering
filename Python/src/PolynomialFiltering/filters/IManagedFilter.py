'''
Created on Mar 13, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.filters.controls import IObservationErrorModel;


class IManagedFilter(ABC):
    def __init__(self,name : str = ''):
        super().__init__(name);
    
    @abstractmethod # pragma: no cover 
    def getGoodnessOfFit(self) -> float:
        pass
    
    @abstractmethod # pragma: no cover
    def add(self, t : float, y : vector, observationId : int = 0) -> bool:    
        pass

    @abstractmethod # pragma: no cover
    def setObservationInverseR(self, inverseR:array) -> None:
        pass
        
    @abstractmethod # pragma: no cover  
    def setObservationErrorModel(self, errorModel : IObservationErrorModel) -> None:
        pass

    
if __name__ == '__main__':
    pass