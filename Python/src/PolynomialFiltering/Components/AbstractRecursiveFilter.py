'''
Created on Feb 13, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import Tuple

from numpy import array, diag, ones, zeros, isscalar

from PolynomialFiltering.Components.IRecursiveFilter import IRecursiveFilter
from PolynomialFiltering.Main import AbstractFilter, FilterStatus


    
class AbstractRecursiveFilter(IRecursiveFilter):
    '''
    classdocs
    '''
    
    #TODO ref
    # factors to compute effective theta from N [RMKdR(???)]
    factors = (2, 3.2, 4.3636, 5.5054, 6.6321, 7.7478)
    
    @classmethod            
    def effectiveTheta(self, order, n : int) -> float:
        if (n < 1 or order < 0 or order > len(AbstractRecursiveFilter.factors)):
            return 0.0
        return 1.0 - AbstractRecursiveFilter.factors[order]/n
        
    def __init__(self, order : int, tau : float ) -> None :
        AbstractFilter.__init__(self)
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported; order %d" % order)
        self.n = 0
        self.n0 = order+1
        self.order = order
        self.dtau = None
        self.t0 = None;
        self.t = None;
        self.Z = None;
        self.tau = tau
        # diagonal matrix D implemented as vector using element-wise operations
        self.D = None   # status denormalization vector D(tau) = [tau^-0, tau^-1,...tau^-order]
#         self.D = array((self.tau*ones([self.order+1]))**(range(0,self.order+1)))
        self.D = zeros([self.order+1])
        for d in range(0,self.order+1):
            self.D[d] = pow(self.tau, d)
        
    def conformState(self, state : array) -> array:
        '''@Z : array'''
        '''@m : int'''
        Z = zeros([self.order+1])
        if isscalar(state) :
            Z[0] = state
        else:
            m = min( self.order+1, len(state))
            Z[0:m] = state[0:m]
        return Z
        
    def start(self, t : float, Z : array) -> None:
        self.n = 0;
        self.t0 = t;
        self.t = t;
        self.Z = self._normalizeState(self.conformState(Z));
    
    def _normalizeTime(self, t : float) -> array:
        return (t - self.t0)/self.tau
    
    def _normalizeDeltaTime(self, dt : float) -> array:
        return dt / self.tau
    
#     def _denormalizeTime(self, n : array) -> array:
#         return self.t0 + n * self.tau
#     
#     def _denormalizeDeltaTime(self, dtau : array) -> array:
#         return dtau * self.tau
#     
    def _denormalizeState(self, Z : array) -> array:
        return Z / self.D
    
    def _normalizeState(self, Z : array) -> array:
        return Z * self.D
    
    def predict(self, t : float) -> Tuple[array, array, array] :
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
#         print(t,dt,dtau)
#         print(AbstractRecursiveFilter.stateTransitionMatrix(self.order+1, dtau))
        Zstar = AbstractRecursiveFilter.stateTransitionMatrix(self.order+1, dtau) @ self.Z
        return (Zstar, dt, dtau)
    
    def update(self, t : float, dtau : array, Zstar : array, e : array) -> None:
        p = self.gammaParameter(t, dtau)
        gamma = self.gamma(p)
#         print(t, Zstar, gamma, p, e)
        self.Z = (Zstar + gamma * e)
        self.t = t
        self.n += 1;
        if (self.n < self.n0) :
            self.setStatus( FilterStatus.INITIALIZING )
        else :
            self.setStatus( FilterStatus.RUNNING )
#         print(self.n, self.t, self.Z)
        
    def getN(self)->int:
        return self.n
    
    def getTau(self) -> float:
        return self.tau
    
    def getTime(self) -> array:
        return self.t
    
    def getState(self, t : float) -> array:
        if (t == self.t) :
            return self._denormalizeState(self.Z)
        else :
            Z = AbstractRecursiveFilter.stateTransitionMatrix(self.order+1, t-self.t) @ self.Z
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
    def gammaParameter(self, t : float, dtau : array) -> array:
        raise NotImplementedError()
            
    @abstractmethod   
    def gamma(self, x : array) -> array:
        raise NotImplementedError()