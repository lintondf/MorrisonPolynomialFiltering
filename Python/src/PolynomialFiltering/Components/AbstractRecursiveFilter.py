'''
Created on Feb 13, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import Tuple

from numpy import array, diag, ones, zeros, isscalar
from scipy.linalg.matfuncs import expm
from PolynomialFiltering.Main import AbstractFilter
from cantera.ctml_writer import state

class IRecursiveFilter(AbstractFilter):
    def __init__(self):
        pass
    
    @abstractmethod   
    def conformState(self, state : array) -> array:
        raise NotImplementedError()

    @abstractmethod   
    def start(self, t : array, Z : array) -> None:
        raise NotImplementedError()
        
    @abstractmethod   
    def predict(self, t : array) -> Tuple[array, array, array] :
        raise NotImplementedError()
 
    @abstractmethod   
    def update(self, t : array, dtau : array, Zstar : array, e : array) -> None:
        raise NotImplementedError()
       
    @abstractmethod   
    def getN(self)->int:
        raise NotImplementedError()
    
    @abstractmethod   
    def getTime(self) -> array:
        raise NotImplementedError()
    
    @abstractmethod   
    def getState(self, t : array) -> array:
        raise NotImplementedError()

    
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
        
    @classmethod            
    def stateTransitionMatrix(self, N : int, dt : float) -> array:
        '''
        Return a Pade' expanded status transition matrix of order m [RMKdR(7)]
            P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
        
        :param N: return matrix is (N,N)
        :param dt: time step
        '''
        B = (diag(ones([N-1]),k=1))
        return expm(dt*B)
    
    def __init__(self, order : int, tau : float ) -> None :
        AbstractFilter.__init__(self)
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported; order %d" % order)
        self.n = 0
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
        Z = zeros([self.order+1])
        if isscalar(state) :
            Z[0] = state
        else:
            m = min( self.order+1, len(state))
            Z[0:m] = state[0:m]
        return Z
        
    def start(self, t : array, Z : array) -> None:
        self.n = 0;
        self.t0 = t;
        self.t = t;
        self.Z = self._normalizeState(self.conformState(Z));
    
    def _normalizeTime(self, t : array) -> array:
        return (t - self.t0)/self.tau
    
    def _normalizeDeltaTime(self, dt : array) -> array:
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
    
    def predict(self, t : array) -> Tuple[array, array, array] :
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        Zstar = AbstractRecursiveFilter.stateTransitionMatrix(self.order+1, dtau) @ self.Z
        return (Zstar, dt, dtau)
    
    def update(self, t : array, dtau : array, Zstar : array, e : array) -> None:
        p = self.gammaParameter(t, dtau)
        gamma = self.gamma(p)
#         print(t, Zstar, gamma, p, e)
        self.Z = (Zstar + gamma * e)
        self.t = t
        self.n += 1;
        
    def getN(self)->int:
        return self.n
    
    def getTau(self) -> float:
        return self.tau
    
    def getTime(self) -> array:
        return self.t
    
    def getState(self, t : array) -> array:
        if (t == self.t) :
            return self._denormalizeState(self.Z)
        else :
            Z = AbstractRecursiveFilter.stateTransitionMatrix(self.order+1, t-self.t) @ self.Z
            return self._denormalizeState(Z)

#     def add(self, t : array, y : array) -> bool:
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
    def gammaParameter(self, t : array, dtau : array) -> array:
        raise NotImplementedError()
            
    @abstractmethod   
    def gamma(self, x : array) -> array:
        raise NotImplementedError()
    
        