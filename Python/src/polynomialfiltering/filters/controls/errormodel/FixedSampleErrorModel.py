''' PolynomialFiltering.filters.controls.FixedSampleErrorModel
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''
from polynomialfiltering.PythonUtilities import constructor, ignore

from numpy import array, isscalar, copy, zeros, transpose
from numpy import array as vector
from numpy.linalg import inv
from polynomialfiltering.Main import AbstractFilterWithCovariance
from polynomialfiltering.filters.controls.IObservationErrorModel import IObservationErrorModel

class FixedSampleErrorModel(IObservationErrorModel):
    '''
        Compute the covariance from a maximum window of (N) observations.
        Return (R0) until M sample have been ingested
    '''

    '''@ R0 : array'''
    '''@ n : int'''
    '''@ N : int'''
    '''@ M : int'''
    '''@ window : array'''
    '''@ R : array''' 
    def __init__(self, R0 : array, N : int, M : int):
        self.R0 = R0
        self.n = 0
        self.N = N
        self.M = M
        self.window = zeros([N, R0.shape[0]])
        self.R = R0
        
    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector) -> array:
        '''@ P : array'''
        '''@ C : array'''
        C = self.getCovarianceMatrix(f, t, y)
        P = inv(C)
        return P; 

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector) -> array:
        '''@ P : array'''
        '''@ L : int'''
        '''@ meanO : array'''
        '''@ i : int'''
        '''@ d : array'''
        L = self.n % self.N
        self.window[L,:] = y
        self.n = self.n + 1;
        if (self.n > self.M) :
            self.R = zeros([self.R0.shape[0], self.R0.shape[1]])
            L = min(self.n, self.N)
            meanO = self.window[0:1,:]
            for i in range(1,L) :
                d = self.window[i:i+1,:] - meanO
                meanO = meanO + (self.window[i:i+1,:]-meanO)/(i+1)
                self.R = self.R + (transpose(d) @ (self.window[i:i+1,:] - meanO) - self.R)/(i+1)
        P = self.R;
        return P; 