''' PolynomialFiltering.filters.controls.ObservationDifferencesErrorModel
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

class ObservationDifferencesErrorModel(IObservationErrorModel):
    '''
    Compute the covariance using a window of (N) observations based on the
    inter-observation differences.  Returns (R0) until (N) observations are
    ingested.
    '''

    
    def __init__(self, R0 : array, N : int):
        self.R0 = R0
        self.n = 0
        self.N = N
        self.window = zeros([N, R0.shape[0]])
        self.R = R0
        
    def getPrecisionMatrix(self, f: AbstractFilterWithCovariance, t:float, y:vector, observationId:int = -1) -> array:
        '''@ P : array'''
        P = inv(self.getCovarianceMatrix(f, t, y, observationId))
        return P; 

    def getCovarianceMatrix(self, f : AbstractFilterWithCovariance, t : float, y : vector, observationId : int = -1) -> array:
        '''@ P : array'''
        self.window[self.n % self.N,:] = y
        self.n = self.n + 1;
        if (self.n > self.N) :
            self.R = zeros([self.R0.shape[0], self.R0.shape[1]])
            for i in range(1,self.N) :
                j1 = (self.n+i) % self.N
                j2 = (self.n+i+1) % self.N
                d = self.window[j2:j2+1,:] - self.window[j1:j1+1,:]
                self.R = self.R + transpose(d) @ d
            self.R = self.R / (2.0*self.N - 2.0)
        if (observationId == -1) :
            P = self.R;
        else :
            P = self.R[observationId:observationId,observationId:observationId]; 
        return P; 
        