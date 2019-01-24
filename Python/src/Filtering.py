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
        P(d)_i,j = (d^(j,i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
'''
def stateTransitionMatrix(N, dt):
    B = (diag(ones([N-1]),k=1))
    return expm(dt*B)

class PBase :
    def __init__(self, order=1) :
        self.order = order
        self.t0 = None
        self.Z = zeros([order+1])
        self.tau = None
        self.dtau = None
        self.D = None               # state denormalization matrix D(tau) = diag[tau^-0, tau^-1,...tau^-order]
        
    def initialize(self, t0, Z0, tau):
        #TODO insure size(Z0) consistent with order
        self.t0 = t0
        self.Z = Z0
        self.tau = tau
        self.D = diag([1.0/(self.tau*ones([self.order+1]))**(range(0,self.order+1))])
    
    def predict(self, dtau):
        P = stateTransitionMatrix(self.order, dtau)
        return P @ self.Z
    
    def error(self, dtau, y):
        return y - self.predict(dtau)
    
    def normalizeTime(self, t):
        return (t - self.t0)/self.tau
    
    def normalizeDeltaTime(self, dt):
        return dt / self.tau
    
    def denormalizeTime(self, n):
        return self.t0 + n * self.tau
    
    def denormalizeDeltaTime(self, dtau):
        return dtau * self.tau
    
class EMP :
    def __init__(self, order=1) :
        self.base = PBase(order)
    
class FMP :
    def __init__(self, order=1) :
        self.base = PBase(order)
    

class ReynekeMorrisonFiltering :
    def __init__(self, order=1) :
        self.emp = EMP(order)
        self.fmp= FMP(order)
        

if __name__ == '__main__':
#     A = array([[0,1,0],[0,0,1], [0,0,0]])
#     print(expm(0.1*A))
#     B = (diag(ones([3-1]),k=1))
#     for n in range(2,6) :
#         print( stateTransitionMatrix(n, 0.1) )
    P = stateTransitionMatrix(3, 0.1)
    X = array([100, 10, 1])
    print(X, P@X )
    print( 1.0/(0.1*ones([3]))**(range(0,3))) # expected D