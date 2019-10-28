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
    switchThreshold = 2.8 # 7.4472 # stats.f.isf(sqrt(p), 1, 1) p=0.5
    restartThreshold = 9.7# 404.62 # stats.f.isf(sqrt(p), 1, 1) p=1e-3
    switchCount = 3
    restartCount = 3
    
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
        self.alpha = 1.0 # 0.05 # Leff = 2/alpha
        self.residuals = zeros([order+1])
        self.iBest = 0
        self.above = zeros([order+1]) # counts of sequentail above threshold
        self.theta = theta;
        self.trace = trace;
    
    @ignore
    def setSwitchThresholdAndCount(self, p : float, c : int):
        self.switchThreshold = zeros([c])
        self.switchCount = c
        for i in range(0, c):
            #TODO handle inf
            self.switchThreshold[i] = stats.f.isf(p**(i+1),1,1)
        if (self.trace != None) :
            self.trace.write('Switch, %d,%10.4g, ' % (self.switchCount, p))
            for i in range(0, c) :
                self.trace.write('%10.4g' % self.switchThreshold[i])
            self.trace.write('\n')
    
    @ignore
    def setRestartThresholdAndCount(self, p : float, c : int):
        self.restartThreshold = zeros([c])
        self.restartCount = c
        for i in range(0, c):
            self.restartThreshold[i] = stats.f.isf(p**(i+1),1,1)
        if (self.trace != None) :
            self.trace.write('Restart, %d, %10.4g, ' % (self.restartCount, p))
            for i in range(0, c) :
                self.trace.write('%10.4g' % self.restartThreshold[i])
            self.trace.write('\n')
        
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
        
        vrfs = zeros([len(self.pairs)])
        innovation = self.pairs[self.iBest].update(t, Zstar, e);
        if (self.pairs[self.iBest].getStatus() == FilterStatus.RUNNING) :
            self.residuals[self.iBest] = (1.0-self.alpha)*self.residuals[self.iBest] + self.alpha * e
            vrfs[self.iBest] = 1.0 + self.pairs[self.iBest].getFirstVRF()
#             if (t > 27.5 and t < 31) :
#                 print(t, self.iBest, self.residuals[4], self.alpha, e)
        o = e + Zstar[0]
        inits = ''
        for i in range(0,len(self.pairs)) :
            if (i != self.iBest) :
                z = self.pairs[i].predict(t)
                f = o - z[0]
#                 if (vrfs[self.iBest] == 0 or self.pairs[i].getStatus() == FilterStatus.RUNNING) :
#                     f = o - z[0]
#                     inits += '-'
#                 else :
#                     inits += '*'
#                     f = Zstar[0] - z[0]
                self.pairs[i].update(t, z, f)
                if (self.pairs[i].getStatus() == FilterStatus.RUNNING) :
                    self.residuals[i] = (1.0-self.alpha)*self.residuals[i] + self.alpha * f
                    vrfs[i] = 1.0 + self.pairs[i].getFirstVRF()
            
        '''
        Find new best pair filter and any filter so bad it must be restarted
        '''
        marker = ' '
        resets = ''
        fs = zeros([len(self.pairs), 1])
        if (vrfs[self.iBest] > 0) : #if best pair has started
            Z = self.getState()
            bestNSSR = self.residuals[self.iBest]**2 # / vrfs[self.iBest]
            bestDof = 1.0# + self.pairs[self.iBest].getOrder()
            for i in range(0, len(self.pairs)) :
                if (i != self.iBest) :
#                     print('%2d, %6.3f, %d, %d, %g, %g' % (self.order, t, self.iBest, i, vrfs[i], vrfs[self.iBest]))
                    if (vrfs[i] > 0) : # and vrfs[i] < 2.0) : # VRF < 1 plus one sigma observation noise
                        dofi = 1.0# + self.pairs[i].getOrder()
                        ssri = self.residuals[i]**2 # / vrfs[i]
                        f = bestNSSR / ssri # (bestNSSR/bestDof) / (ssri/dofi)
                        if (f > self.switchThreshold[0] ) : # self.fthresholds[i, self.iBest]) :
                            fs[i] = f                        
# #                             print('%2d, %6.3f, BETTER %d/%d/%d %14g %14g F %14g %14g' % (self.order, t, self.iBest, self.iNext, i, bestNSSR, ssri, f, self.fthresholds[i, self.iBest]))
                            self.above[i] += 1
                            for j in range(1, self.switchCount) :
                                if (f > self.switchThreshold[j]) :
                                    self.above[i] +=1
                                else :
                                    break;
#                             bestNSSR = ssri
#                         elif (self.iNext == i) : # if this filter was on-deck, but did not remain above threshold
#                             self.iNext = -1
                        elif (f < 1.0/self.restartThreshold[0]) :
                            fs[i] = -1.0/f                        
                            self.above[i] -= 1
                            for j in range(1, self.restartCount) :
                                if (f < 1.0/self.restartThreshold[j]) :
                                    self.above[i] -=1
                                else :
                                    break;
                            if (self.above[i] < -self.restartCount) :
#                                 if (self.trace != None and t > 45 and t < 60) :
#                                     self.trace.write('%2d, %6.3f, RESTART %d from %d : %g, %g, %g\n' % (self.order, t, i, self.iBest, f, ssri, bestNSSR ))
#                                     for j in range(0, len(self.residuals)) :
#                                         self.trace.write('%g/%g, ' % (self.residuals[j] , vrfs[j]))
#                                     self.trace.write('\n')
                                self.pairs[i].start(t, Z)
                                resets += str(i)
                                self.above[i] = 0
                        else :
                            fs[i] = f
                            self.above[i] = 0;
            iNext = self.iBest
            bestF = 1.0
            for i in range(0, len(self.pairs)) :
                if (self.above[i] > self.switchCount) :
                    if (fs[i] > bestF) :
                        iNext = i
                        bestF = fs[i]
            if (iNext != self.iBest) :
#                 if (self.trace != None) :
#                     self.trace.write('%10.3f %d %15.6g %15.6g %15.6g %15.6g %15.6g %15.6g\n' % (t, self.iBest, Z[0], Z[1], Z[2], Z[3], Z[4], Z[5]))
                self.iBest = iNext
#                 if (self.trace != None) :
#                     Y = self.getState()
#                     self.trace.write('%10.3f %d %15.6g %15.6g %15.6g %15.6g %15.6g %15.6g\n' % (t, self.iBest, Y[0], Y[1], Y[2], Y[3], Y[4], Y[5]))
                for j in range(0,len(self.above)) :
                    if (self.above[j] > 0) :
                        self.above[j] = 0
                marker = '*'
        
        if (self.trace != None) :
            self.trace.write('%2d, %6.3f, %s, %2d, ' % (self.order, t, marker, self.iBest))
            for i in range(0, len(self.residuals)) :
                self.trace.write('%10.3g,' % (self.residuals[i]))
            self.trace.write(', ')
            for i in range(0, len(vrfs)) :
                self.trace.write('%8.2g,' % vrfs[i])
            self.trace.write(', ')
            for i in range(0, len(fs)) :
                self.trace.write('%8.2g,' % fs[i])
            self.trace.write(', ')
            self.trace.write( inits )
            self.trace.write(', ')
            for i in range(0, len(self.above)) :
                self.trace.write('%+1d' % self.above[i])
            
            if (len(resets) > 0) :
                self.trace.write(", RESET, %s" % resets)
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