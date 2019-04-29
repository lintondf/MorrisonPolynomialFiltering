''' PolynomialFiltering.components.Fmp
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter


class AbstractCoreFmp(ICore):
    '''
    classdocs
    '''

    '''@theta : float'''
    '''@VRF : array'''

    def __init__(self, tau : float, theta : float):
        '''
        Constructor
        '''
        self.theta = theta;
        self.VRF = self._getVRF(tau, theta);
    
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

    def getVRF(self, n : int) -> array:
        """
        Get the variance reduction matrix
        
        Arguments:
            None
        
        Returns:
            Square matrix (order+1) of input to output variance ratios
        
        """
        return self.VRF;
    
    def getFirstVRF(self, n : int) -> float:
        """
        Get the variance reduction factor for the 0th derivative
        
        Arguments:
            None
        
        Returns:
            0th derivative input to output variance ratio
        """
        '''@V:array'''
        return self.VRF[0,0]
    
    def getLastVRF(self, n : int) -> float:
        """
        Get the variance reduction factor for the 'order'th derivative
        
        Arguments:
            None
        
        Returns:
            'order'th derivative input to output variance ratio
        """
        '''@V:array'''
        return self.VRF[-1,-1]
    
    def getDiagonalVRF(self, n : int) -> array:
        """
        Get the variance reduction matrix diagonal vector for the 'order'th derivative
        
        Arguments:
            None
        
        Returns:
            'order'th derivative input to output variance ratio
        """
        '''@V:array'''
        return diag(diag(self.VRF))
    
    @abstractmethod # pragma: no cover
    def _getVRF(self):
        pass
    
    
class CoreFmp0(AbstractCoreFmp):
    
    def __init__(self, tau : float, theta : float):
        super().__init__(tau, theta)
        
        
