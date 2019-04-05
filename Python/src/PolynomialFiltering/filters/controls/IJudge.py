'''
Created on Apr 5, 2019

@author: NOOK
'''

from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilterWithCovariance


class IJudge(ABC):
    def __init__(self):
        pass

    @abstractmethod # pragma: no cover
    def scalarGOF(self, e : float, innovation : vector, iR : array ) -> float:
        pass

    @abstractmethod # pragma: no cover
    def vectorGOF(self, e : vector, innovation : vector, iR : array ) -> float:
        pass

    
