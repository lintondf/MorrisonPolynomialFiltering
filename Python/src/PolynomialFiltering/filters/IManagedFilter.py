'''
Created on Mar 13, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilterWithCovariance


class IObservationErrorModel(ABC):
    def __init__(self):
        pass

    @abstractmethod # pragma: no cover
    def getInformationMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int) -> array:
        pass
    
    @abstractmethod # pragma: no cover
    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int) -> array:
        pass


class IJudge(ABC):
    def __init__(self):
        pass

    @abstractmethod # pragma: no cover
    def scalarGOF(self, e : float, innovation : vector, iR : array ) -> float:
        pass

    def vectorGOF(self, e : vector, innovation : vector, iR : array ) -> float:
        pass

    
class IMonitor(ABC):
    def __init__(self):
        pass
    
    @abstractmethod # pragma: no cover
    def check(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int, wasEdited : bool ) -> None:
        pass
    
    
    
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