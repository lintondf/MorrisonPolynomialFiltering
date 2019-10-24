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
    
    # switches require two in a row so p*p
    switchThreshold = 4 # 7.4472 # stats.f.isf(sqrt(p), 1, 1) p=0.5
    restartThreshold = 18# 404.62 # stats.f.isf(sqrt(p), 1, 1) p=1e-3
    
    def __init__(self, order : int, tau : float, theta : float, trace=None ) :
        super().__init__(order)
        self.Z = zeros([order+1])
        self.pairs = List()
        v0 = makeFmpCore(0, tau, theta).getFirstVRF(0)
        for i in range(0,order+1) :
            if (i > 0) :
                fc = makeFmpCore(i, tau, theta);
                theta = fc.getThetaForVRF(tau, theta, v0)
                if (i == order) :
                    self.VRF = fc.getVRF(0)
            self.pairs.append( PairedPolynomialFilter(i, tau, theta)) 
        self.alpha = 0.05 # Leff = 2/alpha
        self.residuals = zeros([order+1])
        self.iBest = 0
        self.iNext = -1
        self.theta = theta;
        self.trace = trace;
        
    @ignore
    def setSwitchThreshold(self, t : float):
        self.switchThreshold = t
        
    @ignore
    def setRestartThreshold(self, t : float):
        self.restartThreshold = t
        
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
        vrfs = zeros([len(self.pairs)])
        innovation = self.pairs[self.iBest].update(t, Zstar, e);
        if (self.pairs[self.iBest].getStatus() == FilterStatus.RUNNING) :
            self.residuals[self.iBest] = (1.0-self.alpha)*self.residuals[self.iBest] + self.alpha * e
            vrfs[self.iBest] = 1.0 + self.pairs[self.iBest].getFirstVRF()
        o = e + Zstar[0]
        for i in range(0,len(self.pairs)) :
            if (i != self.iBest) :
                z = self.pairs[i].predict(t)
                f = o - z[0]
                self.pairs[i].update(t, z, f)
                if (self.pairs[i].getStatus() == FilterStatus.RUNNING) :
                    self.residuals[i] = (1.0-self.alpha)*self.residuals[i] + self.alpha * f
                    vrfs[i] = 1.0 + self.pairs[i].getFirstVRF()
            
        '''
        Estimate new best pair filter:
        1.  Never switch to a higher VRF[0,0]
        2.  Find the lowest available smoothed NSSR * VAR(observation)
        '''
        marker = ' '
        resets = ''
        fs = zeros([len(self.pairs), 1])
        if (vrfs[self.iBest] > 0) :
            bestNSSR = self.residuals[self.iBest]**2/vrfs[self.iBest]
            bestDof = 1.0# + self.pairs[self.iBest].getOrder()
            for i in range(0, len(self.pairs)) :
                if (i != self.iBest) :
#                     print('%2d, %6.3f, %d, %d, %g, %g' % (self.order, t, self.iBest, i, vrfs[i], vrfs[self.iBest]))
                    if (vrfs[i] > 0 and vrfs[i] < 2.0) : # VRF < 1 plus one sigma observation noise
                        dofi = 1.0# + self.pairs[i].getOrder()
                        ssri = self.residuals[i]**2/vrfs[i]
                        f = bestNSSR / ssri # (bestNSSR/bestDof) / (ssri/dofi)
                        if (f > self.switchThreshold ) : # self.fthresholds[i, self.iBest]) :
#                             print('%2d, %6.3f, BETTER %d/%d/%d %14g %14g F %14g %14g' % (self.order, t, self.iBest, self.iNext, i, bestNSSR, ssri, f, self.fthresholds[i, self.iBest]))
                            if (self.iNext == i) :
#                                 if (self.trace != None) :
#                                     self.trace.write('%2d, %6.3f, BETTER %d/%d/%d %14g %14g F %14g\n' % (self.order, t, self.iBest, self.iNext, i, bestNSSR, ssri, f))
#                                     self.trace.write('%2d, %6.3f, SWITCH %d -> %d\n' % (self.order, t, self.iBest, i))
                                    
#                                 print('%2d, %6.3f, SWITCH %d -> %d' % (self.order, t, self.iBest, i))
                                self.iBest = i
                                self.iNext = -1
                                marker = '*'
                                # restart all lower order filters
                            else :
                                marker = '?'
                                self.iNext = i
                            bestNSSR = ssri
                        elif (self.iNext == i) : # if this filter was on-deck, but did not remain above threshold
                            self.iNext = -1
#                             break;
            Z = self.pairs[self.iBest].getState()
            for i in range(0, len(self.residuals)) :
                if (i == self.iBest) :
                    continue
                if (vrfs[i] > 0) :
                    ssri = self.residuals[i]**2/vrfs[i]
                    f = ssri / bestNSSR # (bestNSSR/bestDof) / (ssri/dofi)
                    fs[i] = f
                    # reset above threshold filters id
                    #  a switch is not pending (better to compare to new best SSR)
                    if (self.iNext >= 0 and f > self.restartThreshold) :
#                             if (self.trace != None) :
#                                 self.trace.write('%2d, %6.3f, RESTART %d from %d : %g\n' % (self.order, t, i, self.iBest, f))
                        self.pairs[i].start(t, Z)
                        self.residuals[i] = 2.0 * self.residuals[self.iBest] # bias against a switch back
                        fs[i] = -fs[i]
                        resets += str(i)
        if (self.trace != None) :
            self.trace.write('%2d, %6.3f, %s, %2d, %2d, ' % (self.order, t, marker, self.iBest, self.iNext))
            for i in range(0, len(self.residuals)) :
                self.trace.write('%10.3g, ' % (self.residuals[i]))
            self.trace.write(',')
            for i in range(0, len(fs)) :
                self.trace.write('%10.3g, ' % fs[i])
            if (len(resets) > 0) :
                self.trace.write("RESET, %s" % resets)
            self.trace.write('\n')
        return innovation
    
    def getBest(self) -> int:
        return self.iBest
    
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
        n = self.pairs[self.iBest].getOrder()
        self.Z[0:n+1] = self.pairs[self.iBest].getState()
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
        return self.pairs[self.iBest].predict(t)

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