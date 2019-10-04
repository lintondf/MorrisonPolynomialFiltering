''' PolynomialFiltering.filters.AbstractManagedFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import ABC, abstractmethod

from numpy import array
from numpy import array as vector;

from polynomialfiltering.Main import AbstractFilterWithCovariance
from polynomialfiltering.filters.controls.IObservationErrorModel import IObservationErrorModel


class AbstractManagedFilter(AbstractFilterWithCovariance):
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