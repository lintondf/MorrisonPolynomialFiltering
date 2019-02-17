'''
Created on Jan 24, 2019

@author: D. F. Linton, Blue Lightning Development, LLC
'''
from math import sin, pow, ceil, sqrt
from RadarCoordinates import RadarCoordinates
from scipy.stats._continuous_distns import chi2
'''
pip install numpy_ringbuffer
pip install runstats
'''
import os
import sys
import csv
import numpy
import warnings
from math import pi
from scipy.linalg.matfuncs import expm
from numpy.linalg.linalg import solve
from numpy import array, average, var, diag, zeros,\
    ones, argmin, array2string, abs, concatenate, isscalar
from numpy.random import randn
from numpy_ringbuffer import RingBuffer
from scipy.interpolate import PchipInterpolator

from abc import ABC, abstractmethod
from enum import Enum, auto


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits import mplot3d
from runstats import Statistics

import time
from pip._internal.utils.misc import get_installed_distributions


warnings.simplefilter(action='ignore', category=FutureWarning)
# warnings.simplefilter(action='ignore', category=plt.warnings.MatplotlibDeprecationWarning)


'''
'''
def stateTransitionMatrix(N, dt):
    '''
    Return a Pade' expanded status transition matrix of order m [RMKdR(7)]
        P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
    
    :param N: return matrix is (N,N)
    :param dt: time step
    '''
    B = (diag(ones([N-1]),k=1))
    return expm(dt*B)

# def stm(N, dt):
#     B = eye(N)
#     for i in range(0,N) :
#         for j in range(i+1,N):
#             ji = j-i
#             fji = ji
#             for x in range(2,ji) :
#                 fji *= x 
#             B[i,j] = pow(dt,ji)/fji
#     return B

class EditorDefault : 
    def __init__(self, filterBase, editingWindow=15): 
        self.filter = filterBase
        self.n = 0
        self.E = RingBuffer(capacity=editingWindow, dtype=numpy.double)
        self.R = RingBuffer(capacity=editingWindow, dtype=numpy.double)
        
    def reset(self):
        self.n = 0
        self.E = RingBuffer(capacity=self.E.maxlen, dtype=numpy.double)
        self.R = RingBuffer(capacity=self.R.maxlen, dtype=numpy.double)

    def updateResiduals(self, t, y, e):
        '''
        Add residual (observation - prediction) to history
        :param e: observation - prediction
        '''
        self.E.appendleft(e)
        self.R.appendleft(y)
        self.n += 1
        
    def getResidualStatistics(self):
        R = array(self.R)
        r = 0.0
        m = len(R)
        math = self.filter.getMath()
        if (m > 1) :
            for i in range(0, m-1) :
                r += math.square(math.subtract(R[i], R[i+1]))
            r /= 2*m - 2
            return (average(array(self.E)), var(array(self.E)), r)
        else:
            return (0, sys.float_info.max, sys.float_info.max)
    
    def isGoodObservation(self, t, y, e):
        if (self.n >= self.filter.getN0()) :
            self.filter.setStatus(FilterStatus.RUNNING)
        else :
            self.filter.setStatus(FilterStatus.INITIALIZING)            
        return True
    
    
class EditorLocalResiduals(EditorDefault):
    def __init__(self, filterBase, chiSquaredThreshold=3.0, editingWindow=25):
        self.chi2 = chiSquaredThreshold
        EditorDefault.__init__(self, filterBase, editingWindow)    

    def isGoodObservation(self, t, y, e):
        stats = self.getResidualStatistics()
        return (e * 1.0/stats[1] * e) < self.chi2
    
    
class FilterStatus(Enum):
    IDLE = auto()         # Filter is awaiting the first observation    
    INITIALIZING = auto() # Filter has processed one or more observations, but status estimate is not reliable
    RUNNING = auto()      # Filter status estimate is reliable 
    COASTING = auto()     # Filter has not received a recent observation, but the predicted status should be usable
    RESETING = auto()     # Filter coast interval has been exceed and it will reinitialize on the next observation
        
    
class FilterBase(ABC) :
    
    def __init__(self, n0 = 1, editingWindow=15):
        self.t0 = None
        self.t = None
        self.Z = None
        self.n0 = n0  # number of samples required to initialize
        self.setStatus( FilterStatus.IDLE )
        self.editor = EditorDefault(self, editingWindow)
        self.name = ''

    def restart(self, t0, Z0):
        self.t0 = t0
        self.t = t0
        self.Z = Z0
        self.setStatus( FilterStatus.RESETING )
        # self.editor.reset()
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def getEditor(self):
        return self.editor
    
    def getStatus(self):
        return self.status    
        
    def setEditor(self, editor):
        self.editor = editor
        
    def setStatus(self, status):
        self.status = status
        
    def getN(self):
        return self.editor.n
        
    def getN0(self):
        return self.n0
        
    def getGoodnessOfFit(self):
        '''
        Return variance of last (editingWindow) residuals
        '''
        S = self.editor.getResidualStatistics()
        return S[0]**2/S[2]
    
    def getBiasOfFit(self):
        '''
        Return mean of last (editingWindow) residuals
        '''
        return self.editor.getResidualStatistics()[0]
        
    @abstractmethod   
    def getTime(self):
        raise NotImplementedError()
    
    @abstractmethod   
    def getState(self, t):
        raise NotImplementedError()

    @abstractmethod   
    def add(self, t, y):    
        raise NotImplementedError()
    
    
class RecursiveFilterBase(FilterBase) :
    
    # factors to compute effective theta from N [REF???]
    factors = (2, 3.2, 4.3636, 5.5054, 6.6321, 7.7478)
    
    @classmethod            
    def effectiveTheta(self, order, n):
        if (n < 1 or order < 0 or order > len(RecursiveFilterBase.factors)):
            return 0.0
        return 1.0 - RecursiveFilterBase.factors[order]/n
        
    def __init__(self, order, editingWindow=15) :
        FilterBase.__init__(self, order+2, editingWindow)
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported; order %d" % order)
        self.order = order
        self.tau = None
        self.dtau = None
        # diagonal matrix D implemented as vector using element-wise operations
        self.D = None   # status denormalization vector D(tau) = [tau^-0, tau^-1,...tau^-order]
        
    def conformState(self, state):
        Z = zeros([self.order+1])
        n = min( self.order+1, len(state))
        Z[0:n] = state[0:n]
        return Z
        
    def setTau(self, tau):
        self.tau = tau
#         self.D = array((self.tau*ones([self.order+1]))**(range(0,self.order+1)))
        self.D = zeros([self.order+1])
        for d in range(0,self.order+1):
            self.D[d] = pow(self.tau, d)
            
    def initialize(self, t0, Z0, tau):
        self.setTau(tau)
        FilterBase.restart(self, t0, self.D * self.conformState(Z0))
        
    def restart(self, t, Z):
#         print(self.name + ' restart', t, Z)
        FilterBase.restart(self, t, self.D * self.conformState(Z))
    
    def _predict(self, dtau):
        P = stateTransitionMatrix(self.order+1, dtau)
        return P @ self.Z
    
    def _normalizeTime(self, t):
        return (t - self.t0)/self.tau
    
    def _normalizeDeltaTime(self, dt):
        return dt / self.tau
    
    def _denormalizeTime(self, n):
        return self.t0 + n * self.tau
    
    def _denormalizeDeltaTime(self, dtau):
        return dtau * self.tau
    
    def _denormalizeState(self, Z):
        return Z / self.D
    
    def getGoodnessOfFit(self):
        if (self.getN() <= self.order+1) :
            return sys.float_info.max  # with too few samples prefer lower order
        return FilterBase.getGoodnessOfFit(self)
    
    def getTime(self):
        return self.t
    
    def getState(self, t):
        if (t == self.t) :
            return self._denormalizeState(self.Z)
        else :
            Z = stateTransitionMatrix(self.order+1, t-self.t) @ self.Z
            return self._denormalizeState(Z)

    def add(self, t, y):
        if (self.t == None) :
            self.t0 = t
            self.t = t
            self.Z = zeros([self.order+1])
            self.Z[0] = y
        dt = t - self.t
        dtau = self._normalizeDeltaTime(dt)
        Zstar = stateTransitionMatrix(self.order+1, dtau) @ self.Z
        e = (y - Zstar[0])
        self.getEditor().updateResiduals(t, y, e)
        if(self.getEditor().isGoodObservation(t, y, e)) :
            gamma = self.gamma(self.gammaParameter(t, dtau))
            self.Z = (Zstar + gamma * e)
            self.t = t
            return True
        else :
            return False
            
    @abstractmethod   
    def gammaParameter(self, t, dtau):
        raise NotImplementedError()
            
    @abstractmethod   
    def gamma(self, x):
        raise NotImplementedError()
    
class EMPBase(RecursiveFilterBase):    
    def __init__(self, order, editingWindow=15) :
        RecursiveFilterBase.__init__(self, order, editingWindow)
        
    def gammaParameter(self, t, dtau):
        return self._normalizeTime(t)
        

class FMPBase(RecursiveFilterBase) :
    def __init__(self, order=1, theta=0.90) :
        RecursiveFilterBase.__init__(self, order)
        self.theta = theta
    
    def gammaParameter(self, t, dtau):
        return pow(self.theta, abs(dtau))
        
            
class EMP0(EMPBase) :
    def __init__(self, editingWindow=15) :
        EMPBase.__init__(self, 0, editingWindow)
        
    def gamma(self, n):
        return array([1/(1+n)])
    
    def nSwitch(self, theta):
        return 2.0/(1.0-theta)
    
    def VRF(self, n):
        denom = 1.0/((n+1))
        return (1) * denom

    
class EMP1(EMPBase) :
    def __init__(self, editingWindow=15) :
        EMPBase.__init__(self, 1, editingWindow)
        
    def gamma(self, n): #
        denom = 1.0/((n+2)*(n+1))
        return denom*array([2*(2*n+1), 
                            6])
    
    def nSwitch(self, theta):
        return 3.2/(1.0-theta)
    
    def VRF(self, n):
        denom = 1.0/((n+2)*(n+1))
        return (4*n + 6) * denom

class EMP2(EMPBase) :
    def __init__(self, editingWindow=15) :
        EMPBase.__init__(self, 2, editingWindow)
        
    def gamma(self, n): #
        n2 = n*n 
        denom = 1.0/((n+3)*(n+2)*(n+1))
        return denom*array([3*(3*n2+3*n+2), 
                            18*(2*n+1), 
                            (2*1)*30])
    
    def nSwitch(self, theta):
        return 4.3636/(1.0-theta)
    
    def VRF(self, n):
        n2 = n*n 
        denom = 1.0/((n+3)*(n+2)*(n+1))
        return (9*n2 + 27*n + 24) * denom

class EMP3(EMPBase) :
    def __init__(self, editingWindow=15) :
        EMPBase.__init__(self, 3, editingWindow)
        
    def gamma(self, n): #
        n2 = n*n 
        n3 = n2*n 
        denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([8*(2*n3+3*n2+7*n+3), 
                            20*(6*n2+6*n+5), 
                            (2*1)*120*(2*n+1), # 
                            (3*2*1)*140])   # 
    
    def nSwitch(self, theta):
        return 5.50546/(1.0-theta)
    
    def VRF(self, n):
        n2 = n*n 
        denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))
        return (8*(2*n+3)*(n2 + 3*n + 5)) * denom

class EMP4(EMPBase) :
    def __init__(self, editingWindow=15) :
        EMPBase.__init__(self, 4, editingWindow)
        
    def gamma(self, n): # 
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([5*(5*n4+10*n3+55*n2+50*n+24), 
                            25*(12*n3+18*n2+46*n+20), 
                            (2*1)*1050*(n2+n+1), # 
                            (3*2*1)*700*(2*n+1),  # 
                            (4*3*2*1)*630]) #
    
    def nSwitch(self, theta):
        return 6.6321/(1.0-theta)
    
    def VRF(self, n):
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return (25*n4 + 150*n3 + 575*n2 + 1050*n + 720) * denom

class EMP5(EMPBase) :
    def __init__(self, editingWindow=15) :
        EMPBase.__init__(self, 5, editingWindow)
        
    def gamma(self, n):
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([6*(2*n+1)*(3*n4+6*n3+77*n2+74*n+120), 
                            126*(5*n4+10*n3+55*n2+50*n+28), 
                            (2*1)*420*(2*n+1)*(4*n2+4*n+15), #
                            (3*2*1)*1260*(6*n2+6*n+7), #  
                            (4*3*2*1)*3780*(2*n+1),  # 
                            (5*4*3*2*1)*2772]) #
        
    def nSwitch(self, theta):
        return 7.7478/(1.0-theta)
    
    def VRF(self, n):
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return 6*(2*n+3)*(3*n4+18*n3+113*n2+258*n+280) * denom
    
class EMP(FilterBase) :
    emps = [EMP0, EMP1, EMP2, EMP3, EMP4, EMP5]
    
    def __init__(self, order) :
        self.filter = self.emps[order]()
        FilterBase.__init__(self, order+1)
        
    def initialize(self, t0, Z0, tau):
        self.filter.initialize(t0, Z0, tau)
        
    def restart(self, t0, Z0):
        self.filter.restart(t0, Z0)
        
    def getEditor(self):
        return self.filter.editor
    
    def getStatus(self):
        return self.filter.status    
        
    def setEditor(self, editor):
        self.filter.editor = editor
        
    def setStatus(self, status):
        self.filter.status = status
        
    def getN(self):
        return self.filter.editor.n
        
    def getN0(self):
        return self.n0
    
    def VRF(self, n):
        return self.filter.VRF(n)
        
    def nSwitch(self, theta):
        return self.filter.nSwitch(theta)

    def add(self, t, y):
        return self.filter.add(t, y)
        
    def getTime(self):
        return self.filter.getTime()
        
    def getState(self, t):
        return self.filter.getState(t)

    def getBiasOfFit(self):
        return self.filter.getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.filter.getGoodnessOfFit()

        
class EMPSet(FilterBase):        
    '''
    An EMPSet object encapsulates a set of ExpandingMemoryPolynomial filters
    up to the specified order.  All of these filters run in parallel.  The
    filter with the lowest GoodnessOfFit variance is selected to report time,
    status, and fit statistics
    '''
    
    def __init__(self, order, name=''):
        '''
        Initialize this EMPSet object
        :param order: highest order of EMP filter to include
        '''
        self.order = order
        self.emps = []
        self.current = None
        self.gofs = None
        self.setName(name)
        self.settlingFactor = 0.90 #TODO get/set
        for i in range(0, order+1) :
            emp = EMP.emps[i](editingWindow=5)
            emp.setName('%s%d' % (self.name, emp.order))
            self.emps.append(emp)
        FilterBase.__init__(self, order+1)

    def initialize(self, t0, Z0, tau):
        self.current = 0
        self.gofs = zeros([self.order+1])
        for emp in self.emps :
            emp.initialize(t0, Z0[0:0+1], tau)
        
    def restart(self, t0, Z0):
        self.current = 0
        self.gofs = zeros([self.order+1])
        self.emps[self.current].restart(t0, Z0[0:0+1])
        
    def setEditor(self, editor):
        for emp in self.emps :
            emp.setEditor(editor)       

    def getEditor(self):
        return self.emps[self.current].getEditor()
    
    def getStatus(self):
        return self.emps[self.current].getStatus()    
        
    def setStatus(self, status):
        for emp in self.emps :
            emp.setStatus( status )
        
    def getN(self):
        return self.emps[self.current].getN()
        
    def getN0(self):
        return self.emps[self.current].getN0()
        
    def nSwitch(self, theta, which=-1):
        if (which < 0) :
            return self.emps[self.current].nSwitch(theta)
        else :
            return self.emps[which].nSwitch(theta)

    def VRF(self, n):
        return self.emps[self.current].VRF(n)
        
    def add(self, t, y):
        n = self.emps[self.current].getN()
#         if (self.current < self.order) :
#             n = self.emps[self.current].getN()
#             if (n > (self.current+1)**4) :
#                 print('EMPSet switch', n, (self.current+1)**4)
#                 self.emps[self.current+1].restart(self.emps[self.current].getTime(), self.emps[self.current].getState(self.emps[self.current].getTime()))
#                 self.emps[self.current+1].setEditor( self.emps[self.current].getEditor() )
#                 self.current += 1
#         return self.emps[self.current].add(t, y)
        for emp in self.emps :
            emp.add(t, y)
            gof = emp.getGoodnessOfFit()
            self.gofs[emp.order] = gof
        j = argmin(self.gofs)
        r = array2string(self.gofs, formatter={'float_kind':lambda y: "%10.3g" % y})
#         print("%d %10.3g %s from %d (%10.3g) %s" % 
#                   (self.order, t, self.emps[self.current].getName(), self.current, self.gofs[self.current], r))
        if (j > self.current and self.gofs[j] < 1.00*self.gofs[self.current]) :
            print("%d %10.3g %s Switch from %d (%10.3g) to %d (%10.3g) %10.1f" % 
                  (self.order, t, self.emps[self.current].getName(), self.current, self.gofs[self.current], j, self.gofs[j], self.emps[self.current].nSwitch(0.9)))
#             self.emps[j].restart(self.emps[self.current].getTime(), self.emps[self.current].getState(self.emps[self.current].getTime()))
#             self.emps[j].setEditor( self.emps[self.current].getEditor() )
            self.current = j
        return True
        
    def getTime(self):
        return self.emps[self.current].getTime()
        
    def getState(self, t):
        return self.emps[self.current].getState(t)

    def getBiasOfFit(self):
        return self.emps[self.current].getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.emps[self.current].getGoodnessOfFit()
    
    def report(self):
        r = ("%d,%d") % (self.order, self.current)
        for emp in self.emps :
            r += ("{%10.4g, %10.4g} " % (emp.getState(self.getTime())[0], emp.getGoodnessOfFit()))
        r += array2string(self.getState(self.getTime()), formatter={'float_kind':lambda y: "%10.4g" % y})
        return r
    
    def getStates(self):
        t = self.getTime()
        S = zeros([len(self.emps),7])
        for i in range(0,len(self.emps)) :
            s = self.emps[i].getState(t)
            S[i,0:len(s)] = s
        return S
            
    
        
class FMP0(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 0, theta)

    def gamma(self, t):
        return array([1-t])

    def VRF(self, t):
        mt = (1-t)
        pt = (1+t)
        return mt / pt

class FMP1(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 1, theta)

    def gamma(self, t):
        t2 = t*t 
        mt2 = (1-t)*(1-t)
        return array([1-t2, 
                      mt2])

    def VRF(self, t):
        t2 = t*t
        mt = (1-t)
        pt = (1+t)
        pt3 = pt*pt*pt
        return mt*(5 + 4*t + t2) / pt3

class FMP2(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 2, theta)

    def gamma(self, t):
        t2 = t*t
        t3 = t2*t
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        return array([1-t3, 
                      3.0/2.0*mt2 * (1+t),
                      (2*1)*1.0/2.0*mt3])

    def VRF(self, t):
        t2 = t*t
        t3 = t2*t
        t4 = t2*t2 
        mt = (1-t)
        pt = (1+t)
        pt5 = pt*pt*pt*pt*pt
        return mt*(19 + 24*t + 16*t2 + 6*t3 + t4) / pt5

class FMP3(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 3, theta)

    def gamma(self, t):
        t2 = t*t 
        t3 = t2*t
        t4 = t3*t
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        return array([1-t4, 
                      1.0/6.0*mt2 * (11+14*t+11*t2),
                      (2*1)*mt3*(1+t),
                      (3*2*1)*1.0/6.0*mt4])

    def VRF(self, t):
        t2 = t*t
        t3 = t2*t
        t4 = t2*t2 
        t5 = t4*t 
        t6 = t3*t3
        mt = (1-t)
        pt = (1+t)
        pt7 = (pt*pt*pt*pt)*(pt*pt*pt)
        return mt*(69 + 104*t + 97*t2 + 64*t3 + 29*t4 + 8*t5 + t6) / pt7

class FMP4(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 4, theta)

    def gamma(self, t):
        t2 = t*t 
        t3 = t2*t
        t5 = t2*t3
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        return array([1-t5, 
                      5.0/12.0*mt2 * (5+7*t+7*t2+5*t3),
                      (2*1)*5.0/24.0*mt3*(7+10*t+7*t2),
                      (3*2*1)*5.0/12.0*mt4*(1+t),
                      (4*3*2*1)*1.0/24.0*mt4])

    def VRF(self, t):
        t2 = t*t
        t3 = t2*t
        t4 = t2*t2 
        t5 = t4*t 
        t6 = t3*t3
        t7 = t4*t3 
        t8 = t4*t4
        mt = (1-t)
        pt = (1+t)
        pt9 = (pt*pt*pt*pt)*(pt*pt*pt*pt)*pt
        return mt*(251 + 410*t + 446*t2 + 380*t3 + 256*t4 + 130*t5 + 45*t6 + 10*t7 + t8) / pt9

class FMP5(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 5, theta)

    def gamma(self, t):
        t2 = t*t 
        t3 = t2*t
        t4 = t3*t
        t6 = t2*t4
        mt2 = (1-t)*(1-t)
        mt3 = (1-t)*mt2
        mt4 = mt2*mt2
        mt5 = mt3*mt2
        mt6 = mt3*mt3
        return array([1-t6, 
                      1.0/60.0*mt2 * (137+202*t+222*t2+202*t3+137*t4),
                      (2*1)*5.0/8.0*mt3*(1+t)*(3+2*t+3*t2),
                      (3*2*1)*1.0/24.0*mt4*(17+26*t+17*t2),
                      (4*3*2*1)*1.0/8.0*mt5*(1+t),
                      (5*4*3*2*1)*1.0/120.0*mt6 ])
        
    def nSwitch(self):
        return 7.7478/(1.0-self.theta)
 
    def VRF(self, t):
        t2 = t*t
        t3 = t2*t
        t4 = t2*t2 
        t5 = t4*t 
        t6 = t3*t3
        t7 = t4*t3 
        t8 = t4*t4
        t9 = t4*t5
        t10 = t5*t5
        mt = (1-t)
        pt = (1+t)
        pt11 = (pt*pt*pt*pt)*(pt*pt*pt*pt)*(pt*pt*pt)
        return mt*(923 + 1572*t + 1847*t2 + 1792*t3 + 1484*t4 + 1024*t5 + 562*t6 + 232*t7 + 67*t8 + 12*t9 + t10) / pt11

    
class FMP(FilterBase) :
    fmps = [FMP0, FMP1, FMP2, FMP3, FMP4, FMP5]
    
    def __init__(self, order, theta) :
        self.filter = self.fmps[order](theta)
        FilterBase.__init__(self, order+1)
        
    def initialize(self, t0, Z0, tau):
        self.filter.initialize(t0, Z0, tau)
        
    def restart(self, t0, Z0):
        self.filter.restart(t0, Z0)
        
    def getEditor(self):
        return self.filter.editor
    
    def getStatus(self):
        return self.filter.status    
        
    def setEditor(self, editor):
        self.filter.editor = editor
        
    def setStatus(self, status):
        self.filter.status = status
        
    def getN(self):
        return self.filter.editor.n
        
    def getN0(self):
        return self.n0
        
    def add(self, t, y):
#         print(self.getTime(), self.getState(self.getTime()) )
        return self.filter.add(t, y)
        
    def getTime(self):
        return self.filter.getTime()
        
    def getState(self, t):
        return self.filter.getState(t)

    def getBiasOfFit(self):
        return self.filter.getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.filter.getGoodnessOfFit()

    
class FMPSet(FilterBase):        
    '''
    An FMPSet object encapsulates a set of FadingMemoryPolynomial filters
    up to the specified order.  All of these filters run in parallel.  The
    filter with the lowest GoodnessOfFit variance is selected to report time,
    status, and fit statistics
    '''
    
    def __init__(self, order, theta):
        '''
        Initialize this EMPSet object
        :param order: highest order of EMP filter to include
        '''
        self.order = order
        self.fmps = []
        self.current = 0
        self.gofs = None
        for i in range(0, order+1) :
            fmp = FMP.fmps[i](theta)
            fmp.setEditor( EditorDefault(fmp, 10))
            self.fmps.append(fmp)
        FilterBase.__init__(self, order+1)

    def initialize(self, t0, Z0, tau):
        self.current = 0
        self.gofs = zeros([self.order+1])
        for fmp in self.fmps :
            fmp.initialize(t0, Z0[0:fmp.order+1], tau)
        
    def restart(self, t0, Z0):
        self.current = 0
        self.gofs = zeros([self.order+1])
        for fmp in self.fmps :
            fmp.restart(t0, Z0)
        
    def setEditor(self, editor):
        for fmp in self.fmps :
            fmp.setEditor(editor)       

    def getEditor(self):
        return self.fmps[self.current].getEditor()
    
    def getStatus(self):
        return self.fmps[self.current].getStatus()    
        
    def setStatus(self, status):
        for fmp in self.fmps :
            fmp.setStatus( status )
        
    def getN(self):
        return self.fmps[self.current].getN()
        
    def getN0(self):
        return self.fmps[self.current].getN0()
        
    def add(self, t, y):
        for fmp in self.fmps :
            fmp.add(t, y)
            gof = fmp.getGoodnessOfFit()
            self.gofs[fmp.order] = gof
        j = argmin(self.gofs)
#         print(self.gofs)
        if (self.gofs[j] < 0.90*self.gofs[self.current]) :
            print("%d %10.3g Switch from %d (%10.3g) to %d (%10.3g)" % 
                  (self.order, t, self.current, self.gofs[self.current], j, self.gofs[j]))
            self.current = j
        
    def getTime(self):
        return self.fmps[self.current].getTime()
        
    def getState(self, t):
        return self.fmps[self.current].getState(t)

    def getBiasOfFit(self):
        return self.fmps[self.current].getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.fmps[self.current].getGoodnessOfFit()
    
        
class ReynekeMorrison(FilterBase):
    #TODO intercept math and pass to children
    
    def __init__(self, order, theta, name=''):
        self.emp = EMPSet(order, name)
        self.fmp = FMP(order, theta)
        self.current = self.emp
        self.tau = None
        self.n = 0
        self.Ns = ceil(self.emp.nSwitch(theta, order))
        print("Ns", self.Ns)
        self.order = order
        self.theta = theta
        self.setName(name)
        FilterBase.__init__(self, order+1)
  
    def initialize(self, t0, Z0, tau):
        self.tau = tau
        self.emp.initialize(t0, Z0[0:self.order+1], tau)
        self.fmp.initialize(t0, Z0[0:self.order+1], tau)
        
    def restart(self, t0, Z0):
        self.n = 0
        self.emp.filter.restart(t0, Z0)
        self.fmp.filter.restart(t0, Z0)
        
    def setEditor(self, editor):
        self.emp.setEditor(editor)       
        self.fmp.setEditor(editor)       

    def getEditor(self):
        return self.current.getEditor()
    
    def getStatus(self):
        return self.current.getStatus()
        
    def setStatus(self, status):
        self.emp.setStatus( status )
        self.fmp.setStatus( status )
        
    def getN(self):
        return self.n
        
    def getN0(self):
        return self.current.getN0()
        
    def add(self, t, y):
        # print('RM add', self.n, self.Ns )
        if (self.n < self.Ns) :
            if (self.emp.add(t, y)) :
                self.n = self.n + 1
                return True
        elif (self.n == self.Ns) :
            print("%s Switch from EMP to FMP" % (self.name))
            self.fmp.restart(self.emp.getTime(), self.emp.getState(self.emp.getTime()))
            self.fmp.setEditor( self.emp.getEditor() )
            self.current = self.fmp
            if (self.fmp.add(t, y)):
                self.n = self.n + 1
                return True
        else :
            if (self.fmp.add(t, y)):
                self.n = self.n + 1
                return True
        return False
        
    def getTime(self):
        return self.current.getTime()
        
    def getState(self, t):
        return self.current.getState(t)

    def getBiasOfFit(self):
        return self.current.getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.current.getGoodnessOfFit()
    
    def getResidualStatistics(self):
        return self.current.getEditor().getResidualStatistics()
    
  
class FixedMemoryFilter(FilterBase) :
    def __init__(self, length=51) :
        FilterBase.__init__(self)
        self.t = None
        self.Z = []
        self.tRing = RingBuffer(capacity=length, dtype=numpy.double)
        self.yRing = RingBuffer(capacity=length, dtype=numpy.double)
        
    def getTime(self):
        return self.t
    
    def getState(self, t):
        if (t == self.t) :
            return self.Z
        else :
            Z = stateTransitionMatrix(2+1, t-self.getTime()) @ self.Z
            return Z

    def add(self, t, y):    
        self.tRing.appendleft(t)
        self.yRing.appendleft(y)
        if (self.tRing.is_full) :
            T = array(self.tRing)
            Y = array(self.yRing)
            L = len(T)
            TntTn = zeros([3,3]) # Tn' Tn
            TntYn = zeros([3,1]) # Tn' Yn
            for k in range(0,L) :
                dt = T[0] - T[k]
                dt2 = dt*dt
                dt3 = dt2*dt
                dt4 = dt2*dt2
                TntTn[0,0] += 1 
                TntTn[0,1] += -dt 
                TntTn[0,2] += +dt2
                TntTn[1,0] += -dt 
                TntTn[1,1] += +dt2 
                TntTn[1,2] += -dt3
                TntTn[2,0] += +dt2
                TntTn[2,1] += -dt3 
                TntTn[2,2] += +dt4
                TntYn[0,0] += Y[k]
                TntYn[1,0] += -dt*Y[k]
                TntYn[2,0] += dt2*Y[k]
#             Ystar = inv(TntTn) @ TntYn
            Ystar = solve(TntTn, TntYn)
            self.t = T[0]
            self.Z = array([1, 1, 2*1]) * Ystar[:,0]
            self.editor.updateResiduals(t, y, y - self.Z[0])


def generateTestData(order, N, t0, Y0, dt, bias=0.0, sigma=1.0):
    if (order >= 0) :
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N])
        times = zeros([N,1])
        S = stateTransitionMatrix(order+1, dt)
        t = t0 + dt
        Y = Y0
        for i in range(0,N) :
            Y = S @ Y
            observations[i] = Y[0] + noise[i]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    else :
        order = -order
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N]) + noise
        times = zeros([N,1])
        t = t0 + dt
        Y = Y0
        for i in range(0,N) :
            Y[0] = Y0[0] + Y0[1]*sin(0.01*t)
            observations[i] += Y[0]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    return (times, truth, observations, noise)

       
# def fixedMemoryFilter(t, y):
#     # Morrison 1969, pg 297
#     L = len(t)
#     TntTn = zeros([3,3]) # Tn' Tn
#     TntYn = zeros([3,1]) # Tn' Yn
#     for k in range(0,L) :
#         dt = t[0] - t[k]
#         dt2 = dt*dt
#         dt3 = dt2*dt
#         dt4 = dt2*dt2
#         TntTn[0,0] += 1 
#         TntTn[0,1] += -dt 
#         TntTn[0,2] += +dt2
#         TntTn[1,0] += -dt 
#         TntTn[1,1] += +dt2 
#         TntTn[1,2] += -dt3
#         TntTn[2,0] += +dt2
#         TntTn[2,1] += -dt3 
#         TntTn[2,2] += +dt4
#         TntYn[0,0] += y[k]
#         TntYn[1,0] += -dt*y[k]
#         TntYn[2,0] += dt2*y[k]
#     Ystar = inv(TntTn) @ TntYn
#     return array([1, 1, 2*1]) * Ystar[:,0]
     
def testFixedMemoryFilter() :
    N = 101
    y0 = 100.0
    y1 = 10.0
    y2 = 5.0
    Y0 = array([y0, y1, y2, 2.0, 1.0, 0.5]);
    tau = 0.1
    (times, truth, observations) = generateTestData(-5, N, 0.0, Y0, tau, 0.0, 10.0)
    
    fmf = FixedMemoryFilter(11)
    for i in range(0,N) :
        fmf.add(times[i], observations[i])
        if (fmf.getTime() != None) :
            print(i, fmf.getTime(), fmf.getState(fmf.getTime()), truth[i,0:3], fmf.getGoodnessOfFit(), fmf.getBiasOfFit() )
    
def testFMP():        
    N = 100
    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
    (times, truth, observations) = generateTestData(5, N, 0.0, Y0, 0.1)
    fmp = FMPSet(5, 0.95)
    print( fmp.getN0() )
    
    fmp.initialize(0.0, Y0, 0.1)
    for i in range(0,N) :
        fmp.add(times[i][0], truth[i,0])
        Yf = fmp.getState(times[i][0])
        r = array2string(Yf, formatter={'float_kind':lambda y: "%10.4g" % y})
        print("FMPSet %5d %10.4g %10.4g %s %10.4g" % (i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0]))
    
def testReynekeMorrison(theta):
    N = 1000
    order = 5
    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
    (times, truth, observations, noise) = generateTestData(order, N, 0.0, Y0[0:order+1], 0.1,0,10)

    rm = ReynekeMorrison(order, theta)

    rm.initialize(0.0, array([Y0[0]]), 0.1)
    states = zeros([N,order+1])
    S = zeros([N, 3])
    stats = Statistics()
    nstats = Statistics()
    for i in range(0,N) :
        rm.add(times[i][0], observations[i])
        Yf = rm.getState(times[i][0])
        S[i,:] = rm.getResidualStatistics()
        states[i,0:len(Yf)] = Yf
        if (i > N-30) :
            stats.push( Yf[0] - truth[i,0] )
            nstats.push( observations[i] - truth[i,0] )
#         if (i > 700) :
#             r = array2string(Yf, formatter={'float_kind':lambda y: "%10.6g" % y})
#             print("RM %3d %10.4g %10.6g %s %10.4g" %(i, times[i], truth[i,0]-truth[i-1,0], r, S[i,2]))
#         print("RM %5d %10.4g %10.4g %s %10.4g %10.4g %10.4g" % \
#               (i, times[i][0], truth[i,0], r, Yf[0]-truth[i,0], rm.getGoodnessOfFit(), noise[i]))
#     
#     print(S[0:30,:])
#     print(S[-30:,:])
    print(rm.theta, stats.mean()/nstats.mean(), stats.variance()/nstats.variance())
    return (times, states, truth)

if __name__ == '__main__':
    pass
    print(chi2.ppf(0.05,50))
    exit(0)
    for package in get_installed_distributions() :
        print( package)
    exit(0)
    rc = RadarCoordinates();
    E = randn(6,1);
    N = randn(6,1);
    U = randn(6,1);
    print( rc.d1AzimuthdENU1(E, N, U) )
    exit(0)
    with open('../test/landing.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        track = zeros([0,7])
        
        for row in reader :
            R = zeros([1,7])
            R[0,0] = float(row['time'])
            R[0,1] = float(row['east'])
            R[0,2] = float(row['north'])
            R[0,3] = float(row['up'])
            R[0,4] = float(row['azimuth'])
            R[0,5] = float(row['elevation'])
            R[0,6] = float(row['range'])
            track = concatenate([track, R], axis=0)
#         print(track)

        N = 200+0*track.shape[0] # 100+0*
        track = track[0:N,:]
        theta = 0.85
        order = 5
        Y0 = array([0]);
        
        rmAzimuth = ReynekeMorrison(order, theta, 'Az')
        rmElevation = ReynekeMorrison(order, theta, 'El')
        rmRange = ReynekeMorrison(order, theta, 'Rg')
    
        rmAzimuth.initialize(0.0, array([track[0,4]]), 2.72)
        rmElevation.initialize(0.0, array([track[0,5]]), 2.72)
        rmRange.initialize(0.0, array([track[0,6]]), 2.72)
        statesAzimuth = zeros([N,order+1])
        statesElevation = zeros([N,order+1])
        statesRange = zeros([N,order+1])
        
        
        observations = zeros([N,3])
        observations[:,0] = track[:,4] + 5e-5*randn(N)
        observations[:,1] = track[:,5] + 5e-5*randn(N)
        observations[:,2] = track[:,6] + 20*0.3048*randn(N)
        
        P = PchipInterpolator(track[:,0], track[:,6])
        dP = P.derivative()

#         E = EMPSet(5)
#         E.initialize(0.0, array([track[0,6]]), 2.72)
#         
#         rates = zeros([N, 5+2])
#         for i in range(0,N) :
#             E.add(track[i][0], observations[i,2])
#             S = E.getStates()
#             V = S[:,1] # - dP(track[i,0])
#             rates[i,0:len(S[:,1])] = V
#             rates[i,-1] = dP(track[i,0])
#             r = array2string(S[:,1], formatter={'float_kind':lambda y: "%+10.4g" % y})
#             print('%8.2f %10.4g %s' % (track[i][0], dP(track[i,0]), r))
#             
#         fig, ax = plt.subplots()
#         l2 = ax.plot(track[10:,0], rates[10:,2], 'g-' )
#         ax.hold(True)
#         l3 = ax.plot(track[10:,0], rates[10:,3], 'y-' )
#         l4 = ax.plot(track[10:,0], rates[10:,4], 'r-' )
#         l5 = ax.plot(track[10:,0], rates[10:,5], 'b-' )
#         ax.legend(['2', '3', '4', '5'])
#         ax.plot(track[10:,0], rates[10:,-1], 'k-')
#         plt.show()

        V = zeros([N,1])
        for i in range(0,N) :
            V[i] = dP(track[i,0])
            rmAzimuth.add(track[i][0], observations[i,0])
            Yazimuth = rmAzimuth.getState(track[i][0])
            statesAzimuth[i,0:len(Yazimuth)] = Yazimuth
              
            rmElevation.add(track[i][0], observations[i,1])
            Yelevation = rmElevation.getState(track[i][0])
            statesElevation[i,0:len(Yelevation)] = Yelevation
              
            rmRange.add(track[i][0], observations[i,2])
            Yrange = rmRange.getState(track[i][0])
            statesRange[i,0:len(Yrange)] = Yrange
#             print('%5d %10.2f  %12.6g %12.6g %12.6g' % (i, track[i][0], track[i,4], Yazimuth[0], Yazimuth[0] - track[i,4]))

#         fig = plt.figure()
#         ax = plt.axes(projection='3d')
#         ax.plot3D(track[:,4], track[:,5], track[:,6], 'r')
#         for i in range(0,N) :
#             r = array2string(statesAzimuth[i,:], formatter={'float_kind':lambda y: "%+10.4g" % y})
#             r += array2string(statesElevation[i,:], formatter={'float_kind':lambda y: "%+10.4g" % y})
#             r += array2string(statesRange[i,:], formatter={'float_kind':lambda y: "%+10.4g" % y})
#             print("%10.4f %s" % (track[i,0], r))
        fig, ax = plt.subplots()
#         ax.plot(track[:,0], statesRange[:,0], 'b-', track[:,0], observations[:,2], 'r.')
        ax.plot(track[:,0], statesRange[:,1]-V, 'b-')
#         ax.hold(True)
#         ax.plot(track[:,0], V, 'k-')
        plt.show()
        
        
#     testFMP()
#     testFixedMemoryFilter()
#     for theta in range(90, 100) :
#         (times, states, truth) = testReynekeMorrison(0.01*theta)
#     fig, ax = plt.subplots()
#     ax.plot(times[10:], states[10:,0]-truth[10:,0], 'r-') #,times, observations-truth[:,0],'.')
# #     ax.plot(times, (S[:,1]/S[:,2]))
#     plt.show()
#     y0 = 100.0
#     y1 = 10.0
#     y2 = 5.0
#     Y0 = array([y0, y1, y2, 2.0, 1.0, 0.5]);
#     tau = 0.1
#     x = EMP5()
#     x.initialize(0.0, Y0, tau)
#     print(x.D)
#     order = 5
#     print(array((tau*ones([order+1]))**(range(0,order+1))))

#     S1 = stateTransitionMatrix(8, 0.1) - stm(8,0.1)
#     print( array2string(S1, formatter={'float_kind':lambda y: "%6.3g" % y}) )
#     S2 = stm(8, 0.1)
#     print( array2string(S2, formatter={'float_kind':lambda y: "%6.3g" % y}) )
