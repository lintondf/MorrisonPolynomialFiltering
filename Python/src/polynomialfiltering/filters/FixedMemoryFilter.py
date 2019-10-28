''' PolynomialFiltering.components.FixedMemoryFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''
"""
@TODO Morrison 12.2.26, construct from EMP; faster?
"""

from abc import abstractmethod
from overrides import overrides
from polynomialfiltering.PythonUtilities import virtual, inline;

from numpy import array, copy, eye, ones, zeros, transpose
from numpy import array as vector
from numpy.linalg.linalg import solve, lstsq, inv
from scipy.linalg import cho_factor, cho_solve

from polynomialfiltering.Main import AbstractFilter, FilterStatus
from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter


class FixedMemoryFilter(AbstractComponentFilter) :
    """
    Equally-weighted, fixed memory size, irregularly spaced data filter
    
    Same units between state and observations
    """
    
    '''@L :int | number of samples in memory window'''
    '''@n :int | total number of observations processed'''
    '''@n0 :int | number of observations required for valid result'''
    '''@t0 :float | start time of filter'''
    '''@t :float | current time of filter'''
    '''@tau :float | nominal step time of filter'''
    '''@Z :vector | UNNORMALIZED (external units) state vector'''
    '''@tRing :vector | ring buffer holding times of observations'''
    '''@yRing :vector | ring buffer holding values of observations'''
    
    def __init__(self, order : int, memorySize : int = 51 ):
        super().__init__(order);  # TODO name
#         if (order < 0 or order > 5) :
#             raise ValueError("Polynomial orders < 1 or > 5 are not supported") # TODO exceptions
        self.order = order
        self.L = memorySize;
        self.n = 0
        self.n0 = memorySize;
        self.t0 = 0.0;
        self.t = 0.0;
        self.tau = 0.0;
        self.Z = zeros([self.order+1]);
        self.tRing = zeros([memorySize]);
        self.yRing = zeros([memorySize]);
        self.status = FilterStatus.IDLE
        
    @overrides
    def start(self, t : float, Z : vector) -> None:
        pass 
    
    @overrides
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Arguments:
            t - target time
            
        Returns:
            predicted NORMALIZED state (INTERNAL UNITS)
            
        """
        return self.transitionState(t)
    
    @overrides
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ innovation : array'''
        self.add(t, Zstar[0] + e)
        innovation = self.Z - Zstar;
        return innovation; 

    @overrides
    def getN(self)->int:
        return self.n
    
    @overrides
    def getTau(self) -> float:
        return self.tau
    
    @overrides
    def getTime(self) -> float:
        return self.t
    
    def transitionState(self, t : float) -> vector:
        '''@dt : vector : L | array of delta times'''
        '''@Tn : array : L : order+1'''
        '''@Tnt : array : order+1 : L | transpose of Tn'''
        '''@TntTn : array : order+1 : order+1'''
        '''@TntYn : array : order+1 : 1'''
#         print(self.tRing);
#         print(self.yRing)
        dt = self.tRing - t;
        Tn = self._getTn(dt);
        Tnt = transpose(Tn)
        TntTn = Tnt @ Tn;
        TntYn = Tnt @ self.yRing
#         print(TntTn)
#         print(TntYn)
        self.Z = solve(TntTn, TntYn); #cho_solve(cho_factor(TntTn), TntYn); # lstsq(TntTn, TntYn)[0]; #  
        return copy(self.Z);
    
    @overrides
    def getState(self) -> vector:
        return self.transitionState(self.t)
    
    @overrides
    def add(self, t : float, y : float) -> None:
        '''@idx : int'''
        self.t = t;
        idx = self.n % self.L
        self.tRing[ idx ] = t;    
        self.yRing[ idx ] = y;
        self.n += 1;    
        if (self.n > self.L) :
            self.status = FilterStatus.RUNNING
        else :
            self.status = FilterStatus.INITIALIZING
    
    @overrides
    def getVRF(self) -> array:
        '''@V : array'''
        if (self.n < self.L) :
            V = zeros([self.order+1, self.order+1])
        else :
            V = self._transitionVrf(self.t)
        return V
    
    @overrides
    @inline
    def getFirstVRF(self) -> float:
        '''@V : array'''
        V = self.getVRF()
        return V[0,0]

    @overrides
    @inline
    def getLastVRF(self) -> float:
        '''@V : array'''
        V = self.getVRF()
        return V[self.order, self.order]
    
    def _transitionVrf(self, t : float) -> array:
        '''@dt : vector'''
        '''@Tn : array'''
        '''@V : array'''
        dt = self.tRing - t;
        Tn = self._getTn(dt);
        V = inv(transpose(Tn) @ Tn);
        return V
    
    def _getTn(self, dt : vector ) -> array:
        '''@Tn : array'''
        '''@C : vector'''
        '''@fact : float'''
        '''@i : int'''
        Tn = zeros( [dt.shape[0], self.order+1] );
        Tn[:,0:1] = ones([dt.shape[0],1]);
        C = copy(dt);
        fact = 1.0
        for i in range(1, self.order+1) :
            fact /= i;
            Tn[:,i] = C*fact;
            C = C * dt;
        return Tn;


