'''
Created on Mar 27, 2019

@author: NOOK
'''

from abc import abstractmethod

from math import isnan;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from PolynomialFiltering.Components.AbstractRecursiveFilter import AbstractRecursiveFilter
from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import makeEMP, EMPBase
from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import makeFMP, FMPBase

class EmpFmpPair(AbstractRecursiveFilter) :
    
    '''@ emp : EMPBase'''
    '''@ fmp : FMPBase'''
    '''@ current : AbstractRecursiveFilter'''
    
    def __init__(self, order : int, theta : float, tau : float) :
        super().__init__(order, tau);
        self.emp = makeEMP(order, tau);
        self.fmp = makeFMP(order, theta, tau)
        self.current = self.emp;

    def start(self, t : float, Z : vector) -> None:
        self.current = self.emp;
        self.current.start(t, Z)
    
    def predict(self, t : float) -> vector :
        return self.current.predict(t)
    
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ innovation : vector'''
        innovation = self.current.update(t, Zstar, e)
        if (self.current == self.emp) :
            if (self.emp.getN() >= self.emp.nSwitch(self.fmp.getTheta())) :
                self.fmp.copyState( self.emp );
                self.current = self.fmp;
        return innovation;
    
    def getN(self)->int:
        return self.current.getN()
    
    def getTau(self) -> float:
        return self.current.getTau()
    
    def getTime(self) -> float:
        return self.current.getTime()
    
    def getState(self) -> vector:
        return self.current.getState()

    def getVRF(self) -> array:
        return self.current.getVRF()

    def _gammaParameter(self, t : float, dtau : float) -> float: # pragma: no cover
        return 0
    
    def _gamma(self, n : float) -> vector: # pragma: no cover
        return zeros([self.order+1,1])
    
    def _VRF(self) -> array: # pragma: no cover
        return zeros([self.order+1, self.order+1])
