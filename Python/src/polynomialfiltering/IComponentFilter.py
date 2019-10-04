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
    def getTau(self) -> float:
        pass
    
    @abstractmethod   # pragma: no cover
    def start(self, t : float, Z : vector) -> None:
        pass 
    
    @abstractmethod   # pragma: no cover
    def add(self, t : float, y : float) -> None:
        pass
    
    @abstractmethod   # pragma: no cover
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Arguments:
            t - target time
            
        Returns:
            predicted NORMALIZED state (INTERNAL UNITS)
            
        """
        pass
    
    @abstractmethod   # pragma: no cover
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        """
        Update the filter state from using the prediction error e
        
        Arguments:
            t - update time
            Zstar - predicted NORMALIZED state at update time  (INTERNAL UNITS)
            e - prediction error (observation - predicted state)
            
        Returns:
            innovation vector
            
        Examples:
            Zstar = self.predict(t)
            e = observation[0] - Zstar[0]
            self.update(t, Zstar, e )
        """
        pass
    
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
    
        