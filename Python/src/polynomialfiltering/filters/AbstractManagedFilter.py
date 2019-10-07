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
    """
    Extends AbstractFilterWithCovariance to support filter management methods.
    """
    
    def __init__(self, order : int, name : str = ''):
        super().__init__(order, name)
        '''
         Constructor
        
        Arguments:
            order - polynomial order of the filter (state contains order+1 elements)
            name - optional identifying string
        '''
    
    @abstractmethod # pragma: no cover 
    def getGoodnessOfFit(self) -> float:
        pass
    
    @abstractmethod # pragma: no cover
    def addObservation(self, t : float, y : vector) -> bool:    
        pass

    @abstractmethod # pragma: no cover
    def setObservationInverseR(self, inverseR:array) -> None:
        pass
        
    @abstractmethod # pragma: no cover  
    def setObservationErrorModel(self, errorModel : IObservationErrorModel) -> None:
        pass

