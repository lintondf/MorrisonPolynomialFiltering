''' PolynomialFiltering.components.AdaptiveOrderPolynomialFilter
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import Tuple
from abc import abstractmethod
from overrides import overrides
import csv

from math import isnan, exp, log;
from numpy import array, diag, zeros, sqrt, transpose
from numpy import array as vector
from scipy import stats

from polynomialfiltering.Main import FilterStatus
from polynomialfiltering.AbstractComponentFilter import AbstractComponentFilter
from polynomialfiltering.components.Fmp import makeFmpCore
from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter
from polynomialfiltering.PythonUtilities import List, ignore

class AdaptiveOrderPolynomialFilter(AbstractComponentFilter):
    '''
    NSSR is the squared residuals divided by (1 + VRF[0,0])*VAR(observation)
    Note:  The VAR(observations) is unobserved but is the same for all filters in the bank.
    '''

    '''@ iBest : int | current active filter'''
    '''@ iNext : int | filter to become best if confirmed on next cycle; -1 otherwise'''
    '''@ alpha : array | fading factor for SSR exponential smoother'''
    '''@ residuals : array | smoothed (exponential average) observation vs prediction residuals'''
    '''@ fthresholds : array | F-test thresholds[current-order, candidate-order]'''
    '''@ Z : vector | full order state vector (denormalized, EXTERNAL units)'''
    '''@ VRF : array | full order variance reduction matrix'''  
    
    
    def __init__(self, order : int, tau : float, theta : float, trace=None ) :
        super().__init__(order)
        self.Z = zeros([order+1])
        self.pairs = List()
        v0 = makeFmpCore(0, tau, theta).getFirstVRF(0)
        for i in range(0,order+1) :
            if (i > 0) :
                fc = makeFmpCore(i, tau, theta);
#                 theta = fc.getThetaForVRF(tau, theta, v0)
                if (i == order) :
                    self.VRF = fc.getVRF(0)
            self.pairs.append( PairedPolynomialFilter(i, tau, theta)) 
        self.alpha = 2.0/10.0 # 0.05 # Leff = 2/alpha
        self.residuals = zeros([order+1])
        self.variances = zeros([order+1])
        self.weights = zeros([order+1])
        self.weights[0] = 1.0
        self.theta = theta;
        self.trace = trace;
    
    @ignore
    def close(self):
        if (self.trace != None) :
            self.trace.close()
        
    @overrides
    def update(self, t : float, Zstar : vector, e : float) -> vector:
        '''@ z : vector'''
        '''@ innovation : array'''
        '''@ o : float | the observation'''
        '''@ f : float | by filter observation residual'''
        '''@ vrfs : vector | by filter 1+VRF[0,0] zero if filter is not running'''
#         if (self.trace != None) :
#             for i in range(0,len(self.pairs)) :
#                 Z = zeros([5+1])
#                 Z[0:i+1] = self.pairs[i].getState()
#                 self.trace.write('%10.3f %d %15.9g %15.6g %15.6g %15.6g %15.6g %15.6g\n' % (t, i, Z[0], Z[1], Z[2], Z[3], Z[4], Z[5]))
        
        n = len(self.pairs)
        vrfs = zeros([n])
        innovations = zeros([n, self.order+1])
        o = e + Zstar[0] # recover observation
        inits = ''
        for i in range(0,n) :
            z = self.pairs[i].predict(t)
            f = o - z[0]
            innovations[i,0:self.pairs[i].order+1] = self.pairs[i].update(t, z, f)
            if (self.pairs[i].getStatus() == FilterStatus.RUNNING) :
                self.residuals[i] = (1.0-self.alpha)*self.residuals[i] + self.alpha * f
                vrfs[i] = 1.0 + self.pairs[i].getFirstVRF()

        ''' compute weights'''
        S = 0.0            
        for i in range(0,n) :
            if (vrfs[i] > 0 and vrfs[i] < 2) :
                S += 1.0 / self.residuals[i]**2
        self.weights[:] = 0
        self.weights[0] = 1
        for i in range(0,n) :
            if (vrfs[i] > 0 and vrfs[i] < 2) :
                self.weights[i] = 1.0 / (self.residuals[i]**2 * S)
                
        S = 0.0
        for i in range(0,n) :
            if (self.weights[i] > 0 and self.weights[i] < 1.0) :
                if (self.weights[i] > 0.001) :
                    S += 1.0 / self.residuals[i]**2
                theta = self.pairs[i].getTheta();
                if (theta > 0.50 and self.weights[i] < 0.0001) :
                    self.pairs[i].setTheta( max(0.50, 0.99 * theta) )
                elif (theta < self.theta and self.weights[i] > 0.25) :
                    self.pairs[i].setTheta( min(self.theta, 1.0/0.99 * theta) )
        for i in range(0,n) :
            if (self.weights[i] > 0 and self.weights[i] < 1.0) :
                if (self.weights[i] > 0.001) :
                    self.weights[i] = 1.0 / (self.residuals[i]**2 * S)
                else :
                    self.weights[i] = 0.0
                
                
        if (self.trace != None) :
            self.trace.write('%2d, %6.3f, %s, %2d, ' % (self.order, t, '', self.getBest()))
            for i in range(0, len(self.residuals)) :
                self.trace.write('%10.3g,' % (self.residuals[i]))
            self.trace.write(', ')
            for i in range(0, len(vrfs)) :
                self.trace.write('%8.2g,' % vrfs[i])
            self.trace.write(', ')
            for i in range(0, len(self.weights)) :
                self.trace.write('%8.4f,' % self.weights[i])
#             self.trace.write(', ')
#             self.trace.write( inits )
            self.trace.write(', ')
            for i in range(0, len(self.pairs)) :
                self.trace.write('%8.4f' % self.pairs[i].getTheta())
#             
#             if (len(resets) > 0) :
#                 self.trace.write(", RESET, %s" % resets)
            self.trace.write('\n')
        return innovations[0,:]
    
    def getBest(self) -> int:
        iBest = 0
        w = 0
        for i in range(0, len(self.weights)) :
            if (self.weights[i] > w) :
                iBest = i
                w = self.weights[i]
        return iBest
    
    @overrides
    def getStatus(self) -> FilterStatus:
        """
        Return the filter status
        
        Returns:
            FilterStatus enumeration
        """
        return self.pairs[self.iBest].getStatus()    
            

    @overrides
    def start(self, t : float, Z : vector) -> None:
        for i in range(0,len(self.pairs)) :
            self.pairs[self.iBest].start(t, Z)
        
    @overrides
    def getN(self)->int:
        return self.pairs[self.iBest].getN()
    
    @overrides
    def getState(self) -> vector:
        self.Z[:] = 0
        n = len(self.pairs)
        for i in range(0,n) :
            z = self.pairs[i].getState()
            for j in range(0,len(z)) :
                self.Z[j] += self.weights[i] * z[j]
        return self.Z
    
    @overrides
    def getTime(self) -> float:
        return self.pairs[self.iBest].getTime()
    
    @overrides
    def getTau(self) -> float:
        return self.pairs[self.iBest].getTau()

    @overrides
    def add(self, t : float, y : float) -> None:
        '''@Zstar : vector'''
        '''@e : float'''
        Zstar = self.predict(t)
        e = y - Zstar[0]
        self.update(t, Zstar, e)
            
    @overrides
    def predict(self, t : float) -> vector :
        """
        Predict the filter state (Z*) at time t
        
        Arguments:
            t - target time
            
        Returns:
            predicted NORMALIZED state (INTERNAL UNITS)
            
        """
        '''@ Zstar : vector : order+1'''
        '''@ dt : float'''
        '''@ dtau : float'''
        '''@ F : array : order+1 : order+1 '''
        Z = zeros([self.order+1])
        n = len(self.pairs)
        for i in range(0,n) :
            z = self.pairs[i].predict(t)
            for j in range(0,len(z)) :
                Z[j] += self.weights[i] * z[j]
        return Z

    @overrides
    def getFirstVRF(self) -> float:
        self.getVRF()
        return self.VRF[0,0]

    @overrides
    def getLastVRF(self) -> float:
        self.getVRF()
        return self.VRF[-1,-1]
    
    @overrides
    def getVRF(self) -> array:
        n = self.pairs[self.iBest].getOrder()
        self.VRF[0:n+1,0:n+1] = self.pairs[self.iBest].getVRF() 
        return self.VRF      