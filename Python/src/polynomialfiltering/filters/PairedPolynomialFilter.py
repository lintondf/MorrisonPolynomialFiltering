''' PolynomialFiltering.components.PairedPolynomialFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod
from overrides import overrides

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector

from polynomialfiltering.Main import FilterStatus
from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.Emp import makeEmp, nSwitch
from polynomialfiltering.components.Fmp import makeFmpCore

class PairedPolynomialFilter( AbstractComponentFilter ):
    '''@ rpf :RecursivePolynomialFilter | delegate for actual filter processing'''
    '''@ empCore : ICore | provider of core expanding functions'''
    '''@ fmpCore : ICore | provider of core fading functions'''
    '''@ switchN : int '''
    '''@theta : float'''
    
    
    def __init__(self, order : int, tau : float, theta : float ) :
        super().__init__(order)
        self.rpf = makeEmp(order, tau);
        self.empCore = self.rpf.getCore();
        self.fmpCore = makeFmpCore(order, tau, theta);
        self.theta = theta;
        self.switchN = int(nSwitch( self.order, self.theta ))
        
    @overrides
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ i : array'''
        i = self.rpf.update(t, Zstar, e);
        if (self.rpf.getN() == self.switchN) :
            self.rpf.setCore( self.fmpCore );
        return i
    
    @overrides
    def getStatus(self) -> FilterStatus:
        """
        Return the filter status
        
        Returns:
            FilterStatus enumeration
        """
        return self.rpf.getStatus()    
            

    @overrides
    def start(self, t : float, Z : vector) -> None:
        self.rpf.setCore(self.empCore)
        self.rpf.start(t, Z)

        
    def isFading(self) -> bool:
        '''@isF : bool'''
        isF = self.rpf.getN() >= self.switchN
        return isF
        
    @overrides
    def getN(self)->int:
        return self.rpf.getN()
    
    @overrides
    def getState(self) -> vector:
        return self.rpf.getState()
    
    @overrides
    def getTime(self) -> float:
        return self.rpf.getTime()
    
    @overrides
    def getTau(self) -> float:
        return self.rpf.getTau()

    @overrides
    def add(self, t : float, y : float) -> None:
        '''@Zstar : vector'''
        '''@e : float'''
        Zstar = self.predict(t)
        e = y - Zstar[0]
        self.update(t, Zstar, e)
            
    @overrides
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Arguments:
            t - target time
            
        Returns:
            predicted NORMALIZED state (INTERNAL UNITS)
            
        """
        '''@ Zstar : vector : order+1'''
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ F : array : order+1 : order+1 '''
        return self.rpf.predict(t)

    @overrides
    def getFirstVRF(self) -> float:
        return self.rpf.getFirstVRF()

    @overrides
    def getLastVRF(self) -> float:
        return self.rpf.getLastVRF()
    
    @overrides
    def getVRF(self) -> array:
        return self.rpf.getVRF()