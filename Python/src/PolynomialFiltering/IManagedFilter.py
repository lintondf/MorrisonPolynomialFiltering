'''
Created on Mar 13, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod
from enum import Enum
from numpy import array, eye, zeros, isscalar
from numpy import array as vector;


class IObservationErrorModel(ABC):
    def __init__(self):
        pass

    @abstractmethod   
    def getInverseCovariance(self, t : float, y : vector, observationId : str) -> array:
        pass
    

    
    
class IManagedFilter(ABC):
    def __init__(self,name : str = ''):
        super().__init__(name);
    
    @abstractmethod   
    def getGoodnessOfFit(self) -> float:
        pass
    
    @abstractmethod   
    def add(self, t : float, y : vector, observationId : str = '') -> None:    
        pass

    @abstractmethod   
    def addWithVariance(self, t : float, y : vector, inverseR : array, observationId : str = '') -> None:    
        pass
    
    @abstractmethod   
    def addWithErrorModel(self, t : float, y : vector, errorModel : IObservationErrorModel, observationId : str = '') -> None:    
        pass
    
if __name__ == '__main__':
    pass