'''
Created on Apr 5, 2019

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


