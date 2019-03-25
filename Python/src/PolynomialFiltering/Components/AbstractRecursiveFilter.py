'''
Created on Feb 13, 2019

@author: NOOK
'''

from abc import abstractmethod
from typing import Tuple

from numpy import array, diag, eye, ones, zeros, isscalar, transpose, array_equal
from numpy import array as vector;

from PolynomialFiltering.Components.IRecursiveFilter import IRecursiveFilter
from PolynomialFiltering.Main import AbstractFilter, FilterStatus

from TestUtilities import nearPD, A2S
    
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
#         super().__init__(self)
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported")
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
            
    def _conformState(self, state : vector) -> vector:
        '''@Z : vector'''
        '''@m : int'''
        Z = zeros([self.order+1])
        m = min( self.order+1, len(state) )
        Z[0:m] = state[0:m]
        return Z
        
    def start(self, t : float, Z : vector) -> None:
        self.n = 0;
        self.t0 = t;
        self.t = t;
        self.Z = self._normalizeState(self._conformState(Z));
    
    def _normalizeTime(self, t : float) -> float:
        return (t - self.t0)/self.tau
    
    def _normalizeDeltaTime(self, dt : float) -> float:
        return dt / self.tau
    
    def _normalizeState(self, Z : vector) -> vector:
        return Z * self.D
    
    def _denormalizeState(self, Z : vector) -> vector:
        return Z / self.D
    
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Args:
            t - target time
            
        Returns:
            A three tuple holding: (predicted-NORMALIZED-state, delta-time, delta-tau)
            
        Examples:
            Zstar = self.predict(t)
        """
        '''@ Zstar : vector'''
        
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ F : array'''
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        F = self.stateTransitionMatrix(self.order+1, dtau)
        Zstar = F @ self.Z;
#         Zstar = self.stateTransitionMatrix(self.order+1, dtau) @ self.Z
        return Zstar;
    
    def update(self, t : float, Zstar : vector, e : float) -> None:
        """
        Update the filter state from using the prediction error e
        
        Args:
            t - update time
            Zstar - predicted NORMALIZED state at update time
            e - prediction error (observation - predicted state)
            
        Returns:
            None
            
        Examples:
            Zstar = self.predict(t)
            e = observation[0] - Zstar[0]
            self.update(t, Zstar, e )
        """
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ p : float'''
        '''@ gamma : vector'''
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        p = self._gammaParameter(t, dtau)
        gamma = self._gamma(p)
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
            '''@F : array'''
            F = self.stateTransitionMatrix(self.order+1, self._normalizeDeltaTime(t-self.t));
            Z = F @ self.Z
            return self._denormalizeState(Z)

    def getCovariance(self, t : float, R : float = 1.0) -> array:
        '''@ V : vector'''
        V = self._VRF();
        if (V[0,0] == 0) :
            return V;
        if (t == (self.t + self.tau)) :
            return V * R;
        else :
            '''@F : array'''
            # the VRF equations used are for 1-step predictors
            F = self.stateTransitionMatrix(self.order+1, self._normalizeDeltaTime(t-(self.t+self.tau))); # (self.t+self.tau)-t
            V = transpose(F) @ V @ F;
            return V * R;

    @abstractmethod   
    def _gammaParameter(self, t : float, dtau : float) -> float:
        pass
            
    @abstractmethod   
    def _gamma(self, nOrT : float) -> vector:
        pass

    @abstractmethod
    def _VRF(self) -> array:
        pass
