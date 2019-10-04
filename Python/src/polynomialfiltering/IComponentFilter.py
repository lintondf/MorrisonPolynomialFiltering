''' PolynomialFiltering.polynomialfiltering.IComponentFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import ABC, abstractmethod
from enum import Enum
from numpy import array, eye, transpose, zeros
from numpy import array as vector;
from polynomialfiltering.PythonUtilities import virtual, forcestatic;

class IComponentFilter(ABC):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @abstractmethod   # pragma: no cover
    def getFirstVRF(self) -> float:
        """
        Get the variance reduction factor for the 0th derivative
        
        Arguments:
            None
        
        Returns:
            0th derivative input to output variance ratio
        """
        pass

    @abstractmethod   # pragma: no cover
    def getLastVRF(self) -> float:
        """
        Get the variance reduction factor for the 'order'th derivative
        
        Arguments:
            None
        
        Returns:
            'order'th derivative input to output variance ratio
        """
        pass
    
    @abstractmethod   # pragma: no cover
    def getVRF(self) -> array:
        pass
    
    @abstractmethod   # pragma: no cover
    def add(self, t : float, y : float, observationId : int = -1) -> None:
        pass
    
        