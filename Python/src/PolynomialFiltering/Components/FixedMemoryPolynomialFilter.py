'''
Created on Feb 18, 2019

@author: NOOK
'''

from typing import Tuple
from abc import abstractmethod

from numpy import array, diag, zeros, transpose
from PolynomialFiltering.Components.AbstractRecursiveFilter import IRecursiveFilter
from scipy.special import binom

class FixedMemoryBase(IRecursiveFilter) :
    
    def __init__(self, order : int, memorySize=51 ) -> None:
        super().__init__();  # TODO name
        self.order = order;
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 1 or > 5 are not supported; order %d" % order)
        self.L = memorySize;
        self.n = 0
        self.n0 = order+1
        self.t0 = None;
        self.t = None;
        self.Z = None;
        
    def getN(self)->int:
        return self.n
    
    def getTau(self) -> float:
        return self.tau
    
    def getTime(self) -> array:
        return self.t
    
    def getState(self, t : float) -> array:
        pass
    
    def _getTn(self, dt : float ) -> array:
        Tn = zeros( [dt.shape[0], self.order+1] );
        Tn[:,0] = 1.0;
        C = -dt;
        for i in range(1, self.order+1) :
            Tn[:,i] = C;
            C *= dt;
        return Tn;

if __name__ == '__main__':
    dt = -0.1;
    F = zeros([6,6]);
    for i in range(0,F.shape[0]) : 
        for j in range(i,F.shape[1]) :
            F[i,j] = binom(j,i) * dt**(j-i);
    print(F);
    M = zeros([1, F.shape[0]]);
    M[0,0] = 1;
    print(M)
    print( M @ F )
    fixed = FixedMemoryBase(2, 11);
    dt = zeros([11]);
    for d in range(0, 11) :
        dt[d] = -d * 0.1;
    print(fixed._getTn(dt))
    print( 0 == None)
    