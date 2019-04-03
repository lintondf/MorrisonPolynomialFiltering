'''
Created on Feb 18, 2019

@author: NOOK
'''

from abc import abstractmethod

from numpy import array, copy, eye, ones, zeros, transpose
from numpy import array as vector
from numpy.linalg.linalg import solve, lstsq, inv

from PolynomialFiltering.Main import AbstractFilterWithCovariance, FilterStatus

class FixedMemoryFilter(AbstractFilterWithCovariance) :
    """
    Equally-weighted, fixed memory size, irregularly spaced data filter
    
    Same units between state and observations
    """
    
    '''@order :int | order of fitted polynomial'''
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
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 1 or > 5 are not supported") # TODO exceptions
        self.L = memorySize;
        self.n = 0
        self.n0 = memorySize;
        self.t0 = 0.0;
        self.t = 0.0;
        self.tau = 1.0;
        self.Z = zeros([self.order+1]);
        self.tRing = zeros([memorySize]);
        self.yRing = zeros([memorySize]);
        
    def getN(self)->int:
        return self.n
    
    def getTau(self) -> float:
        return self.tau
    
    def getTime(self) -> float:
        return self.t
    
    def transitionState(self, t : float) -> vector:
        '''@dt : vector | array of delta times'''
        '''@Tn : array'''
        '''@Tnt : array | transpose of Tn'''
        '''@TntTn : array'''
        '''@TntYn : array'''
        dt = self.tRing - t;
        Tn = self._getTn(dt);
        Tnt = transpose(Tn)
        TntTn = Tnt @ Tn;
        TntYn = Tnt @ self.yRing
        self.Z = solve(TntTn, TntYn); # lstsq(TntTn, TntYn, rcond=None)[0];
        return self.Z;
    
    def getState(self) -> vector:
        return self.transitionState(self.t)
    
    def add(self, t : float, y : float, observationId : str = '') -> None:
        self.t = t;
        self.tRing[ self.n % self.L ] = t;    
        self.yRing[ self.n % self.L ] = y;
        self.n += 1;    
    
    def getCovariance(self) -> array:
        return self.transitionCovariance(self.t)
    
    def transitionCovariance(self, t : float) -> array:
        '''@dt : vector'''
        '''@Tn : array'''
        dt = self.tRing - t;
        Tn = self._getTn(dt);
        return inv(transpose(Tn) @ Tn);
    
    def _getTn(self, dt : vector ) -> array:
        '''@Tn : array'''
        '''@C : vector'''
        '''@fact : float'''
        '''@i : int'''
        Tn = zeros( [dt.shape[0], self.order+1] );
        Tn[:,0] = ones([dt.shape[0]]);
        C = copy(dt);
        fact = 1.0
        for i in range(1, self.order+1) :
            fact /= i;
            Tn[:,i] = C*fact;
            C = C * dt;
        return Tn;



# if __name__ == '__main__':
# #     dt = -0.1;
# #     F = zeros([6,6]);
# #     for i in range(0,F.shape[0]) : 
# #         for j in range(i,F.shape[1]) :
# #             F[i,j] = binom(j,i) * dt**(j-i);
# #     print(F);
# #     M = zeros([1, F.shape[0]]);
# #     M[0,0] = 1;
# #     print(M)
# #     print( M @ F )
#     fixed = FixedMemoryFilter(3, 11);
#     dt = zeros([11]);
#     for d in range(0, 11) :
#         dt[d] = -d * 0.1;
#     Tn = fixed._getTn(dt);
#     TntYn = transpose(Tn) @ dt;
#     TntTn = transpose(Tn) @ Tn;
#     print(solve(TntTn, TntYn) )
#     print( inv(TntTn) @ TntYn)
#     iR = diag(0.1*ones([11]));
#     TntiRTn = transpose(Tn) @ iR @ Tn;
#     TntiRYn = transpose(Tn) @ iR @ dt;
#     print(solve(TntiRTn, TntiRYn) )
#     print(inv(TntiRTn)@TntiRYn )
