'''
Created on Apr 5, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilterWithCovariance

class IMonitor(ABC):
    def __init__(self):
        pass
    
    @abstractmethod # pragma: no cover
    def check(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int, wasEdited : bool ) -> None:
        pass
    
    
    
