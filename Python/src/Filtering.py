'''
Created on Jan 24, 2019

@author: D. F. Linton, Blue Lightning Development, LLC
'''

import numpy
import warnings
from scipy.linalg.matfuncs import expm
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astropy.coordinates.funcs import concatenate
from numpy import array, empty, concatenate, flip, average, std, diag, zeros,\
    ones, transpose, multiply
import statsmodels.api as sm

'''
    Pade' expanded state transition matrix of order m [RMKdR(7)]
        P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
'''
def stateTransitionMatrix(N, dt):
    B = (diag(ones([N]),k=1))
    return expm(dt*B)

class PBase :
    def __init__(self, order=1) :
        if (order < 0 or order > 5) :
            raise ValueError("Polynomial orders < 0 or > 5 are not supported; order %d" % order)
        self.order = order
        self.t0 = None
        self.t = None
        self.Z = zeros([order+1])
        self.tau = None
        self.dtau = None
        # diagonal matrix D implemented as vector using element-wise operations
        self.D = None   # state denormalization vector D(tau) = [tau^-0, tau^-1,...tau^-order]
        
    def initialize(self, t0, Z0, tau):
        if (len(Z0) != self.order+1) :
            raise ValueError("Z0 must be a vector of %d elements" % (self.order+1))
        self.tau = tau
        self.D = array((self.tau*ones([self.order+1]))**(range(0,self.order+1)))
        self.t0 = t0
        self.t = t0
        self.Z = self.D * Z0 # normalize initial state vector
    
    def predict(self, dtau):
        P = stateTransitionMatrix(self.order, dtau)
        return P @ self.Z
    
    def normalizeTime(self, t):
        return (t - self.t0)/self.tau
    
    def normalizeDeltaTime(self, dt):
        return dt / self.tau
    
    def denormalizeTime(self, n):
        return self.t0 + n * self.tau
    
    def denormalizeDeltaTime(self, dtau):
        return dtau * self.tau
    
    def denormalizeState(self, Z):
        return Z / self.D
    
    def gamma(self, x):
        raise NotImplementedError()
    
    def add(self, t, y):
        dt = t - self.t
        dtau = self.normalizeDeltaTime(dt)
#         print("add1 ", dt, dtau)
#         print("Z", self.Z)
        Zstar = stateTransitionMatrix(self.order, dtau) @ self.Z
#         print("Z*", Zstar)
        e = y - Zstar[0]
#         print("e",e)
        n = self.normalizeTime(t)
        gamma = self.gamma(n)
#         print(n, gamma)
        self.Z = Zstar + gamma * e
        self.t = t
        return self.denormalizeState(self.Z)
        
class EMP0(PBase) :
    def __init__(self) :
        PBase.__init__(self, 0)
        
    def gamma(self, n):
        return array([1/(1+n)])
    
    
class EMP1(PBase) :
    def __init__(self) :
        PBase.__init__(self, 1)
        
    def gamma(self, n):
        denom = (n+2)**-2
        return denom*array([2*(2*n+1), 
                            6])
    
class EMP2(PBase) :
    def __init__(self) :
        PBase.__init__(self, 2)
        
    def gamma(self, n):
        denom = (n+3)**-3
        return denom*array([3*(3*n**2+3*n+2), 
                            18*(2*n+1), 
                            (2*1)*30])
    
class EMP3(PBase) :
    def __init__(self) :
        PBase.__init__(self, 3)
        
    def gamma(self, n):
        denom = (n+4)**-4
        return denom*array([8*(2*n**3+3*n**2+7*n+3), 
                            20*(6*n**2+6*n+5), 
                            (2*1)*120*(2*n-1), 
                            (3*2*1)*140])
    
class EMP4(PBase) :
    def __init__(self) :
        PBase.__init__(self, 4)
        
    def gamma(self, n):
        denom = (n+5)**-5
        return denom*array([5*(5*n**4+10*n**3+55*n**2+50*n+24), 
                            25*(12*n**3+18*n**2+46*n+20), 
                            (2*1)*1050*(n**2+n+1), 
                            (3*2*1)*700*(2*n+1), 
                            (4*3*2*1)*630])
    
class EMP5(PBase) :
    def __init__(self) :
        PBase.__init__(self, 5)
        
    def gamma(self, n):
        denom = (n+6)**-6
        return denom*array([6*(2*n+1)*(3*n**4+6*n**3+77*n**2+74*n+120), 
                            126*(5*n**4+10*n**3+55*n**2+50*n+28), 
                            (2*1)*420*(2*n+1)*(4*n**2+4*n+15), 
                            (3*2*1)*1260*(6*n**2+6*n+7), 
                            (4*3*2*1)*3780*(2*n+1), 
                            (5*4*3*2*1)*2772])
    
    
class FMP(PBase) :
    def __init__(self, order=1) :
        PBase.__init__(self, order)
    

class ReynekeMorrisonFiltering :
    def __init__(self, order=1) :
        pass
#         self.emp = EMP(order)
#         self.fmp= FMP(order)
        

if __name__ == '__main__':
#     A = array([[0,1,0],[0,0,1], [0,0,0]])
#     print(expm(0.1*A))
#     B = (diag(ones([3-1]),k=1))
#     for n in range(2,6) :
#         print( stateTransitionMatrix(n, 0.1) )
    base = PBase(2)
    base.initialize(0.0, (array([100.0, 10.0, 1.0])), 0.1)
    print(base.normalizeDeltaTime(0.1))
    P = stateTransitionMatrix(2, base.normalizeDeltaTime(0.1))
    print(P)
    print(base.D)
    X = array([100.0, 10.0, 1.0])
    nX = base.D * X
    print( X, nX, P @ nX, (P @ nX) / base.D)
#     X = array([100, 10, 1])
# #     print(X.ndim, X.shape, P@X )
# #     print( 1.0/(0.1*ones([3]))**(range(0,3))) # expected D
#     order = 2
#     tau = 0.1
#     D = array(1.0/(tau*ones([order+1]))**(range(0,order+1)))
#     print(D)
#     print(len(D))
#     print(D.ndim)
#     print(diag(D,0))
    n = 4
    print(n**-2)