'''
Created on Mar 13, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod
from enum import Enum
from numpy import array, eye, zeros, isscalar
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilter;


class IManagedFilter(AbstractFilter):
    def __init__(self,name : str = ''):
        super().__init__(name);
    
    @abstractmethod   
    def getGoodnessOfFit(self) -> float:
        pass
    
    @abstractmethod   
    def getBiasOfFit(self) -> float:
        pass
        
    @abstractmethod   
    def add(self, t : float, y : vector, observationId : str = '') -> None:    
        pass

    @abstractmethod   
    def addWithVariance(self, t : float, y : vector, R : array, observationId : str = '') -> None:    
        pass
    
    @abstractmethod   
    def getCovariance(self, t : float) -> array:
        pass

if __name__ == '__main__':
    pass