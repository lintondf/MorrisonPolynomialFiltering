'''
Created on Sep 27, 2019

@author: lintondf
'''

''' PolynomialFiltering.filters.controls.WindowedEmpErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from polynomialfiltering.PythonUtilities import constructor, ignore, List

from numpy import array, isscalar, copy, zeros, transpose, diag
from numpy import array as vector
from numpy.linalg import inv
from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.filters.controls.IObservationErrorModel import IObservationErrorModel

from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter

class PairResidualsErrorModel(IObservationErrorModel):
    '''
        Compute the covariance from a maximum window of (N) observations based of residuals of 
        an (order) Expanding Memory Polynomial filter.
        Return (R0) when filter status is not RUNNING
    '''

    '''@ R0 : array'''
    '''@ n : int'''
    '''@ m : int'''
    '''@ N : int'''
    '''@ tRing : array'''
    '''@ yRing : array'''
    '''@ filters : List[PairedPolynomialFilter]'''
    '''@ R : array''' 
    
    def __init__(self, R0 : array, memorySize : int, order : int, tau : float, theta : float):
        '''@ i : int'''
        self.R0 = R0
        self.m = R0.shape[0]
        self.n = 0
        self.N = memorySize
        self.tRing = zeros([memorySize, 1]);
        self.yRing = zeros([memorySize, self.m]);        
        self.filters = List()
        for i in range(0,self.m) : 
            self.filters.append(PairedPolynomialFilter(order, tau, theta))
        self.R = R0
        
    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector) -> array:
        '''@ P : array'''
        '''@ C : array'''
        C = self.getCovarianceMatrix(f, t, y)
        P = inv(C)
        return P; 

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector) -> array:
        '''@ P : array'''
        '''@ idx : int'''
        '''@ i : int'''
        '''@ L : int'''
        '''@ k : int'''
        '''@ ie : int'''
        '''@ E : array'''
        '''@ yp : vector'''
        '''@ meanO : array'''
        '''@ d : array'''
        '''@ F : PairedPolynomialFilter'''
        idx = self.n % self.N
        self.tRing[ idx, 0 ] = t;    
        self.yRing[ idx, : ] = y;
        self.n += 1;    
        if (self.n == 1) :
            for i in range(0, self.m) :
                F = self.filters[i]
                F.start(t, y[i:i+1])
            return self.R
        L = min(self.n, self.N)
        k = 0
        for ie in range(0, self.m) :
            F = self.filters[ie]
            F.add(t, y[ie])
        if (self.filters[0].getStatus() == FilterStatus.RUNNING and self.filters[0].getFirstVRF() < 0.5) :
            for i in range(0, L) :
                E = zeros([1,self.m])
                self.R = zeros([self.m, self.m])
                for ie in range(0, self.m) :
                    F = self.filters[ie]
                    yp = F.transitionState(self.tRing[i])
                    E[0,ie] = self.yRing[i, ie] - yp[0]
                if (k == 0) :
                    meanO = E
                    self.R = zeros([self.m, self.m])
                else :
                    d = E - meanO
                    meanO = meanO + (E-meanO)/(k+1)
                    self.R = self.R + (transpose(d) @ (E - meanO) - self.R)/(k+1)
                k += 1
        return self.R
    
    @ignore
    def dump(self):
        print('t, Y ', self.n, self.n % self.N)
        for j in range(0,self.N) :
            print(j, self.tRing[j, 0], self.yRing[j,:])
#         print('S')
#         for i in range(0,self.S.shape[0]) :
#             print('%5d: %14.6g %14.6g, %14.6g, %15.1f  %14.6g' % (i, self.S[i,0], self.S[i,1], self.S[i,2], self.S[i,3], self.S[i,4] ))
#         print('E')
#         for i in range(0,self.E.shape[0]) :
#             print(i, self.E[i,:])
