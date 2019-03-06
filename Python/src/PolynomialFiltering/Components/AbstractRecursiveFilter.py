'''
Created on Feb 13, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import Tuple

from numpy import array, diag, ones, zeros, isscalar
from numpy import array as vector;

from PolynomialFiltering.Components.IRecursiveFilter import IRecursiveFilter
from PolynomialFiltering.Main import AbstractFilter, FilterStatus


    
class AbstractRecursiveFilter(IRecursiveFilter):
    '''
    classdocs
    '''
    
    '''@ order : int'''  # TODO why not auto inherited?
    '''@ n : int'''
    '''@ n0 : int'''
    '''@ dtau : float'''
    '''@ t0 : float'''
    '''@ tau : float'''
    '''@ t : float'''
    '''@ Z : vector'''
    '''@ D : vector'''
            
    @classmethod            
    def effectiveTheta(self, order : int, n : float) -> float:
        '''@factor : float'''
        if (n < 1):
            return 0.0
        factor = 1.148*order + 2.0367;
        return 1.0 - factor/n
    
    def __init__(self, order : int, tau : float ) -> None :
        super().__init__(self)
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported; order %d" % order)
        self.n = 0
        self.n0 = order+1
        self.order = order
        self.dtau = 0
        self.t0 = 0;
        self.t = 0;
        self.Z = zeros([self.order+1]);
        self.tau = tau
        # diagonal matrix D implemented as vector using element-wise operations
        # status denormalization vector D(tau) = [tau^-0, tau^-1,...tau^-order]
        self.D = zeros([self.order+1])
        '''@ d : int'''
        for d in range(0,self.order+1):
            self.D[d] = pow(self.tau, d)
        
    def conformState(self, state : vector) -> vector:
        '''@Z : vector'''
        '''@m : int'''
        Z = zeros([self.order+1])
#         if isscalar(state) :
#             Z[0] = state
#         else:
        m = min( self.order+1, len(state) )
        Z[0:m] = state[0:m]
        return Z
        
    def start(self, t : float, Z : vector) -> None:
        self.n = 0;
        self.t0 = t;
        self.t = t;
        self.Z = self._normalizeState(self.conformState(Z));
    
    def _normalizeTime(self, t : float) -> float:
        return (t - self.t0)/self.tau
    
    def _normalizeDeltaTime(self, dt : float) -> float:
        return dt / self.tau
    
#     def _denormalizeTime(self, n : array) -> array:
#         return self.t0 + n * self.tau
#     
#     def _denormalizeDeltaTime(self, dtau : array) -> array:
#         return dtau * self.tau
#     
    def _denormalizeState(self, Z : vector) -> vector:
        return Z / self.D
    
    def _normalizeState(self, Z : vector) -> vector:
        return Z * self.D
    
    def predict(self, t : float) -> Tuple[vector, float, float] :
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ Zstar : vector'''
        
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        Zstar = self.stateTransitionMatrix(self.order+1, dtau) @ self.Z
        return (Zstar, dt, dtau)
    
    def update(self, t : float, dtau : float, Zstar : vector, e : vector) -> None:
        '''@ p : float'''
        '''@ gamma : vector'''
        p = self.gammaParameter(t, dtau)
        gamma = self.gamma(p)
        self.Z = (Zstar + gamma * e)
        self.t = t
        self.n += 1;
        if (self.n < self.n0) :
            self.setStatus( FilterStatus.INITIALIZING )
        else :
            self.setStatus( FilterStatus.RUNNING )
        
    def getN(self)->int:
        return self.n
    
    def getTau(self) -> float:
        return self.tau
    
    def getTime(self) -> float:
        return self.t
    
    def getState(self, t : float) -> vector:
        '''@ Z : vector'''
        if (t == self.t) :
            return self._denormalizeState(self.Z)
        else :
            Z = self.stateTransitionMatrix(self.order+1, t-self.t) @ self.Z
            return self._denormalizeState(Z)

#     def add(self, t : float, y : array) -> bool:
#         dt = t - self.t
#         dtau = self._normalizeDeltaTime(dt)
#         Zstar = AbstractRecursiveFilter.stateTransitionMatrix(self.order+1, dtau) @ self.Z
#         e = (y - Zstar[0])
#         self.getEditor().updateResiduals(t, y, e)
#         if(self.getEditor().isGoodObservation(t, y, e)) :
#             gamma = self.gamma(self.gammaParameter(t, dtau))
#             self.Z = (Zstar + gamma * e)
#             self.t = t
#             return True
#         else :
#             return False
            
    @abstractmethod   
    def gammaParameter(self, t : float, dtau : float) -> float:
        raise NotImplementedError()
            
    @abstractmethod   
    def gamma(self, nOrT : float) -> vector:
        raise NotImplementedError()