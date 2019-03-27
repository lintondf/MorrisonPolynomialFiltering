'''
Created on Feb 18, 2019

@author: NOOK
'''

from abc import abstractmethod

from numpy import array, copy, ones, zeros, transpose
from numpy import array as vector
from numpy.linalg.linalg import solve, lstsq, inv

from PolynomialFiltering.Main import AbstractFilter, FilterStatus

class FixedMemoryFilter(AbstractFilter) :
    
    '''@order :int'''
    '''@L :int'''
    '''@n :int'''
    '''@n0 :int'''
    '''@t0 :float'''
    '''@t :float'''
    '''@tau :float'''
    '''@Z :vector'''
    '''@tRing :vector'''
    '''@yRing :vector'''
    
    def __init__(self, order : int, memorySize : int = 51 ) -> None:
        super().__init__();  # TODO name
        self.order = order;
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 1 or > 5 are not supported")
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
        '''@dt : vector'''
        '''@Tn : array'''
        '''@Tnt : array'''
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
        return self.getMidpoint(self.t)
    
    def add(self, t : float, y : float, observationId : str = '') -> None:
        self.t = t;
        self.tRing[ self.n % self.L ] = t;    
        self.yRing[ self.n % self.L ] = y;
        self.n += 1;    
    
    def getCovariance(self, R : float = 1.0) -> array:
        return self.transitionCovariance(self.t, R)
    
    def transitionCovariance(self, t : float, R : float = 1.0) -> array:
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
