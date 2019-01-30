'''
Created on Jan 24, 2019

@author: D. F. Linton, Blue Lightning Development, LLC
'''
from math import sin, pow
'''
pip install numpy_ringbuffer
pip install runstats
'''
import sys
import numpy
import warnings
from scipy.linalg.matfuncs import expm
from numpy.linalg.linalg import inv, solve
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astropy.coordinates.funcs import concatenate
from numpy import array, empty, concatenate, flip, average, std, var, diag, zeros,\
    ones, transpose, multiply, argmin, fliplr, flipud, eye, array2string
from numpy.linalg import norm
from numpy.random import randn
import statsmodels.api as sm
from runstats import Statistics
from numpy_ringbuffer import RingBuffer

from abc import ABC, abstractmethod
from enum import Enum, auto

'''
'''
def stateTransitionMatrix(N, dt):
    '''
    Return a Pade' expanded state transition matrix of order m [RMKdR(7)]
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
    def __init__(self, filterBase, editingWindow=25): 
        self.filter = filterBase
        self.n = 0
        if (editingWindow > 0) :
            self.E = zeros([editingWindow])
        else :
            self.E = []
        
    def reset(self):
        self.n = 0
        if (len(self.E) > 0) :
            self.E = 0*self.E

    def updateResiduals(self, e):
        '''
        Add residual (observation - prediction) to history
        :param e: observation - prediction
        '''
        if (len(self.E) > 0) :
            self.E[self.n % len(self.E)] = e
        self.n += 1
        
    def getResidualStatitics(self):
        if (len(self.E) > 0) :
            m = min(len(self.E), self.n)
            return (average(self.E[0:m]), var(self.E[0:m]))
        else :
            return (0.0, sys.float_info.max)
    
    def isGoodObservation(self, t, y, e):
        if (self.n >= self.filter.n0) :
            self.filter.setState(FilterStates.RUNNING)
        else :
            self.filter.setState(FilterStates.INITIALIZING)            
        return True
    
    
class EditorLocalResiduals(EditorDefault):
    def __init__(self, filterBase, chiSquaredThreshold=3.0, editingWindow=25):
        self.chi2 = chiSquaredThreshold
        EditorDefault.__init__(self, filterBase, editingWindow)    

    def isGoodObservation(self, t, y, e):
        stats = self.getResidualStatitics()
        return (e * 1.0/stats[1] * e) < self.chi2
    
    
class FilterStates(Enum):
    IDLE = auto()         # Filter is awaiting the first observation    
    INITIALIZING = auto() # Filter has processed one or more observations, but state estimate is not reliable
    RUNNING = auto()      # Filter state estimate is reliable 
    COASTING = auto()     # Filter has not received a recent observation, but the predicted state should be usable
    RESETING = auto()     # Filter coast interval has been exceed and it will reinitialize on the next observation
        
        
class FilterBase(ABC) :
    
    def __init__(self, n0 = 1):
        self.t0 = None
        self.t = None
        self.Z = None
        self.n0 = n0  # number of samples required to initialize
        self.state = FilterStates.IDLE
        self.editor = EditorDefault(self)

    def restart(self, t0, Z0):
        self.t0 = t0
        self.t = t0
        self.Z = Z0
        self.state = FilterStates.RESETING
        self.editor.reset()
        
    def setEditor(self, editor):
        self.editor = editor
        
    def setState(self, state):
        self.state = state
        
    def getGoodnessOfFit(self):
        '''
        Return variance of last (editingWindow) residuals
        '''
        return self.editor.getResidualStatitics()[1]
    
    def getBiasOfFit(self):
        '''
        Return mean of last (editingWindow) residuals
        '''
        return self.editor.getResidualStatitics()[0]
        
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
    def __init__(self, order) :
        FilterBase.__init__(self, order+1)
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported; order %d" % order)
        self.order = order
        self.tau = None
        self.dtau = None
        # diagonal matrix D implemented as vector using element-wise operations
        self.D = None   # state denormalization vector D(tau) = [tau^-0, tau^-1,...tau^-order]
        
    def setTau(self, tau):
        self.tau = tau
#         self.D = array((self.tau*ones([self.order+1]))**(range(0,self.order+1)))
        self.D = zeros([self.order+1])
        for d in range(0,self.order+1):
            self.D[d] = pow(self.tau, d)
        
    def initialize(self, t0, Z0, tau):
        if (len(Z0) < self.order+1) :
            raise ValueError("Z0 must be a vector of at least %d elements" % (self.order+1))
        self.setTau(tau)
        FilterBase.restart(self, t0, self.D * Z0[0:self.order+1])
        
    def restart(self, t, Z):
        FilterBase.restart(self, t, self.D * Z[0:self.order+1])
    
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
        if (self.editor.n <= self.order+1) :
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
        e = y - Zstar[0]
        self.editor.updateResiduals(e)
        if(self.editor.isGoodObservation(t, y, e)) :
            gamma = self.gamma(self.gammaParameter(t, dtau))
            self.Z = Zstar + gamma * e
            self.t = t
            
    @abstractmethod   
    def gammaParameter(self, t, dtau):
        raise NotImplementedError()
            
    @abstractmethod   
    def gamma(self, x):
        raise NotImplementedError()
    
class EMPBase(RecursiveFilterBase):    
    def __init__(self, order) :
        RecursiveFilterBase.__init__(self, order)
        
    def gammaParameter(self, t, dtau):
        return self._normalizeTime(t)
        

class FMPBase(RecursiveFilterBase) :
    def __init__(self, order=1, theta=0.90) :
        RecursiveFilterBase.__init__(self, order)
        self.theta = theta
    
    def gammaParameter(self, t, dtau):
        return pow(self.theta, abs(dtau))
        
            
class EMP0(EMPBase) :
    def __init__(self) :
        EMPBase.__init__(self, 0)
        
    def gamma(self, n):
        return array([1/(1+n)])
    
    def nSwitch(self, theta):
        return 2.0/(1.0-theta)
    
    
class EMP1(EMPBase) :
    def __init__(self) :
        EMPBase.__init__(self, 1)
        
    def gamma(self, n): #
        denom = 1.0/((n+2)*(n+1))
        return denom*array([2*(2*n+1), 
                            6])
    
    def nSwitch(self, theta):
        return 3.2/(1.0-theta)
    
class EMP2(EMPBase) :
    def __init__(self) :
        EMPBase.__init__(self, 2)
        
    def gamma(self, n): #
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+3)*(n+2)*(n+1))
        return denom*array([3*(3*n2+3*n+2), 
                            18*(2*n+1), 
                            (2*1)*30])
    
    def nSwitch(self, theta):
        return 4.3636/(1.0-theta)
    
class EMP3(EMPBase) :
    def __init__(self) :
        EMPBase.__init__(self, 3)
        
    def gamma(self, n): #
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([8*(2*n3+3*n2+7*n+3), 
                            20*(6*n2+6*n+5), 
                            (2*1)*120*(2*n+1), 
                            (3*2*1)*140])
    
    def nSwitch(self, theta):
        return 5.50546/(1.0-theta)
    
class EMP4(EMPBase) :
    def __init__(self) :
        EMPBase.__init__(self, 4)
        
    def gamma(self, n): # 
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([5*(5*n4+10*n3+55*n2+50*n+24), 
                            25*(12*n3+18*n2+46*n+20), 
                            (2*1)*1050*(n2+n+1), 
                            (3*2*1)*700*(2*n+1), 
                            (4*3*2*1)*630])
    
    def nSwitch(self, theta):
        return 6.6321/(1.0-theta)
    
class EMP5(EMPBase) :
    def __init__(self) :
        EMPBase.__init__(self, 5)
        
    def gamma(self, n):
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return denom*array([6*(2*n+1)*(3*n4+6*n3+77*n2+74*n+120), 
                            126*(5*n4+10*n3+55*n2+50*n+28), 
                            (2*1)*420*(2*n+1)*(4*n2+4*n+15), 
                            (3*2*1)*1260*(6*n2+6*n+7), 
                            (4*3*2*1)*3780*(2*n+1), 
                            (5*4*3*2*1)*2772])
        
    def nSwitch(self, theta):
        return 7.7478/(1.0-theta)
    
    def VRF(self, n):
        n2 = n*n 
        n3 = n2*n 
        n4 = n2*n2
        denom = 1.0/((n+6)*(n+5)*(n+4)*(n+3)*(n+2)*(n+1))
        return 6*(2*n+3)*(3*n4+18*n3+113*n2+258*n+280) * denom
    
class EMP() :
    emps = [EMP0, EMP1, EMP2, EMP3, EMP4, EMP5]
    
    def __init__(self, order) :
        self.filter = self.emps[order]()
        
    def initialize(self, t0, Z0, tau):
        self.filter.initialize(t0, Z0, tau)
        
    def restart(self, t0, Z0):
        self.filter.restart(t0, Z0)
        
    def setEditor(self, editor):
        self.filter.setEditor(editor)      
        
    def nSwitch(self, theta):
        return self.filter.nSwitch(theta)

    def add(self, t, y):
        self.filter.add(t, y)
        
    def getTime(self):
        return self.filter.getTime()
        
    def getState(self, t):
        return self.filter.getState(t)

    def getBiasOfFit(self):
        return self.filter.getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.filter.getGoodnessOfFit()

        
class EMPSet():        
    '''
    An EMPSet object encapsulates a set of ExpandingMemoryPolynomial filters
    up to the specified order.  All of these filters run in parallel.  The
    filter with the lowest GoodnessOfFit variance is selected to report time,
    state, and fit statistics
    '''
    
    def __init__(self, order):
        '''
        Initialize this EMPSet object
        :param order: highest order of EMP filter to include
        '''
        self.order = order
        self.emps = []
        self.current = None
        self.gofs = None
        for i in range(0, order+1) :
            self.emps.append(EMP.emps[i]())

    def initialize(self, t0, Z0, tau):
        self.current = 0
        self.gofs = zeros([self.order+1])
        for emp in self.emps :
            emp.initialize(t0, Z0[0:emp.order+1], tau)
        
    def restart(self, t0, Z0):
        self.current = 0
        self.gofs = zeros([self.order+1])
        for emp in self.emps :
            emp.filter.restart(t0, Z0)
        
    def setEditor(self, editor):
        for emp in self.emps :
            emp.setEditor(editor)       

    def nSwitch(self, theta):
        return self.emps[self.current].nSwitch(theta)

    def add(self, t, y):
        for emp in self.emps :
            emp.add(t, y)
            gof = emp.getGoodnessOfFit()
            self.gofs[emp.order] = gof
        j = argmin(self.gofs)
        if (j > self.current and self.gofs[j] < 0.90*self.gofs[self.current]) :
            print("%d %10.3g Switch from %d (%10.3g) to %d (%10.3g) %10.1f" % 
                  (self.order, t, self.current, self.gofs[self.current], j, self.gofs[j], self.emps[self.current].nSwitch(0.9)))
            self.current = j
        
    def getTime(self):
        return self.emps[self.current].getTime()
        
    def getState(self, t):
        return self.emps[self.current].getState(t)

    def getBiasOfFit(self):
        return self.emps[self.current].getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.emps[self.current].getGoodnessOfFit()
    
        
class FMP0(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 0, theta)

    def gamma(self, t):
        return array([1-t])

class FMP1(FMPBase):    
    def __init__(self, theta=0.9) :
        FMPBase.__init__(self, 1, theta)

    def gamma(self, t):
        t2 = t*t 
        mt2 = (1-t)*(1-t)
        return array([1-t2, 
                      mt2])

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
 
    
class FMP() :
    fmps = [FMP0, FMP1, FMP2, FMP3, FMP4, FMP5]
    
    def __init__(self, order) :
        self.filter = self.fmps[order]()
        
    def initialize(self, t0, Z0, tau):
        self.filter.initialize(t0, Z0, tau)
        
    def restart(self, t0, Z0):
        self.filter.restart(t0, Z0)
        
    def setEditor(self, editor):
        self.filter.setEditor(editor)      
        
    def add(self, t, y):
        self.filter.add(t, y)
        
    def getTime(self):
        return self.filter.getTime()
        
    def getState(self, t):
        return self.filter.getState(t)

    def getBiasOfFit(self):
        return self.filter.getBiasOfFit()
    
    def getGoodnessOfFit(self):
        return self.filter.getGoodnessOfFit()

    
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
            self.editor.updateResiduals(y - self.Z[0])


def generateTestData(order, N, t0, Y0, dt, bias=0.0, sigma=1.0):
    if (order >= 0) :
        truth = zeros([N,order+1])
        observations = bias + sigma*randn(N,1)
        times = zeros([N,1])
        S = stateTransitionMatrix(order+1, dt)
        t = t0 + dt
        Y = Y0
        for i in range(0,N) :
            Y = S @ Y
            observations[i] += Y[0]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    else :
        order = -order
        truth = zeros([N,order+1])
        observations = bias + sigma*randn(N,1)
        times = zeros([N,1])
        t = t0 + dt
        Y = Y0
        for i in range(0,N) :
            Y[0] = sin(t)
            observations[i] += Y[0]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    return (times, truth, observations)

       
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
    
if __name__ == '__main__':
    pass
#     testFixedMemoryFilter()
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

    S1 = stateTransitionMatrix(8, 0.1) - stm(8,0.1)
    print( array2string(S1, formatter={'float_kind':lambda y: "%6.3g" % y}) )
    S2 = stm(8, 0.1)
    print( array2string(S2, formatter={'float_kind':lambda y: "%6.3g" % y}) )
