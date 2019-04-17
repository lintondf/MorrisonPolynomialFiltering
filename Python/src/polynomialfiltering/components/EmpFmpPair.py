''' PolynomialFiltering.components.EmpFmpPair
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from abc import abstractmethod

from math import isnan;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter
from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import makeEMP, EMPBase
from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import makeFMP, FMPBase

class EmpFmpPair(AbstractRecursiveFilter) :
    """
    Filter composed of an expanding memory and a fading memory filter of the same order.
    
    The EMP filter is used to initialize and after the sample number when the 0th order
    variance of the EMP filter matches that variance of the FMP at the configured theta
    fading factor, we switch to the FMP filter. See Morrison 1969, Section 13.8
    """
    
    '''@ emp : EMPBase'''
    '''@ fmp : FMPBase'''
    '''@ current : AbstractRecursiveFilter'''
    
    def __init__(self, order : int, theta : float, tau : float) :
        super().__init__(order, tau);
        """
        Constructor
        
        Arguments:
            order - integer polynomial orer
            theta - fading factor
            tau - nominal time step        
        """
        self.emp = makeEMP(order, tau);
        self.fmp = makeFMP(order, theta, tau)
        self.current = self.emp;

    def start(self, t : float, Z : vector) -> None:
        """@super"""
        self.current = self.emp;
        self.current.start(t, Z)
    
    def predict(self, t : float) -> vector :
        """@super"""
        return self.current.predict(t)
    
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        """@super"""
        '''@ innovation : vector'''
        innovation = self.current.update(t, Zstar, e)
        if (self.current == self.emp) :
            if (self.emp.getN() >= self.emp.nSwitch(self.fmp.getTheta())) :
                self.fmp.copyState( self.emp );
                self.current = self.fmp;
        return innovation;
    
    def getN(self)->int:
        """@super"""
        return self.current.getN()
    
    def getTau(self) -> float:
        """@super"""
        return self.current.getTau()
    
    def getTime(self) -> float:
        """@super"""
        return self.current.getTime()
    
    def getState(self) -> vector:
        """@super"""
        return self.current.getState()

    def getVRF(self) -> array:
        """@super"""
        return self.current.getVRF()

    def _gammaParameter(self, t : float, dtau : float) -> float: # pragma: no cover
        """@none | stub to meet interface; never used"""
        return 0
    
    def _gamma(self, n : float) -> vector: # pragma: no cover
        """@none | stub to meet interface; never used"""
        return zeros([self.order+1,1])
    
    def _VRF(self) -> array: # pragma: no cover
        """@none | stub to meet interface; never used"""
        return zeros([self.order+1, self.order+1])
