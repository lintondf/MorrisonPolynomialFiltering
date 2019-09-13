''' PolynomialFiltering.components.ICore
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import ABC, abstractmethod
from polynomialfiltering.PythonUtilities import virtual, inline;

from numpy import array, zeros;
from numpy import array as vector;


class ICore(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod # pragma: no cover
    def getSamplesToStart(self) -> int:
        """
        Get the number of input samples needed to start this core

        Returns:
            sample count
        """
        pass   

    @abstractmethod # pragma: no cover   
    def getGamma(self, t : float, dtau : float) -> vector:
        """
        Get the innovation scale vector
        
        Arguments:
            t - external time
            dtau - internal step
        
        Returns:
            vector (order+1) of (observation-predict) multipliers
        """
        pass

    @abstractmethod # pragma: no cover
    def getVRF(self, n : int) -> array:
        """
        Get the variance reduction matrix
        
        Arguments:
            None
        
        Returns:
            Square matrix (order+1) of input to output variance ratios
        
        """
        pass
    
    @abstractmethod # pragma: no cover
    def getFirstVRF(self, n : int) -> float:
        """
        Get the variance reduction factor for the 0th derivative
        
        Arguments:
            None
        
        Returns:
            0th derivative input to output variance ratio
        """
        pass
    
    @abstractmethod # pragma: no cover
    def getLastVRF(self, n : int) -> float:
        """
        Get the variance reduction factor for the 'order'th derivative
        
        Arguments:
            None
        
        Returns:
            'order'th derivative input to output variance ratio
        """
        pass
    

