'''
Created on Feb 15, 2019

@author: NOOK
'''

import time
from netCDF4 import Dataset
from math import sin, cos
import numpy as np
from numpy import array, array2string, diag, eye, ones, zeros, sqrt
from numpy.random import randn
from scipy.linalg.matfuncs import expm
from scipy.stats import chi2
from scipy.stats._continuous_distns import norm
from PolynomialFiltering.Main import AbstractFilter

def createTestGroup(cdf : Dataset, name : str ) -> Dataset:
    return cdf.createGroup(name);

def writeTestVariable(group : Dataset, name : str, data : array) -> None:
    dims = data.shape;
    if (len(dims) == 1) :
        dims = (dims[0], 1);
    nDim = '%s_N' % name;
    mDim = '%s_M' % name;
    group.createDimension(nDim, dims[0]);
    group.createDimension(mDim, dims[1]);
    v = group.createVariable(name, 'd', (nDim, mDim))
    v[:] = data;



# def stateTransitionMatrix(N : int, dt : float) -> array:
#     '''
#     Return a Pade' expanded status transition matrix of order m [RMKdR(7)]
#         P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
#     
#     :param N: return matrix is (N,N)
#     :param dt: time step
#     '''
#     B = (diag(ones([N-1]),k=1))
#     return expm(dt*B)

def stateTransitionMatrix(N : int, dt : float) -> array:        
    B = (diag(ones([N-1]),k=1))
    return expm(dt*B)

def generateTestData(order, N, t0, Y0, dt, bias=0.0, sigma=1.0):
    ''' (times, truth, observations, noise)
        times N by 1
        truth N by order+1
        observations N by 1
        noise N by 1 '''
    if (order >= 0) :
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N,1])
        times = zeros([N,1])
        S = stateTransitionMatrix(order+1, dt)
        t = t0
        Y = Y0
        for i in range(0,N) :
            times[i] = t
            truth[i,:] = Y[:]
            observations[i] = Y[0] + noise[i]
            Y = S @ Y
            t = t+dt
    else :
        order = -order
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N]) + noise
        times = zeros([N,1])
        t = t0
        Y = Y0
        for i in range(0,N) :
            Y[0] = Y0[0] + Y0[1]*sin(0.01*t)
            observations[i] += Y[0]
            times[i] = t
            truth[i,:] = Y[:]
            t = t+dt
    return (times, truth, observations, noise)

def isChi2Valid( varSample, varPopulation, N, p=0.05 ) :
    y = (N-1) * varSample/varPopulation;
    yl = chi2.ppf(p, N)
    yu = chi2.ppf(1.0-p, N)
    return y >= yl and y <= yu

def A2S( A : array, format="%10.3g" ) -> str:
    return array2string(A, formatter={'float_kind':lambda y: format % y}, max_line_width=256)

def box_m(n_1,C0,n_2,C1):

    global Xp

    m = 2
    k = 2 # len(np.cov(X0))
#     n_1 = len(X0[0])
#     n_2 = len(X1[0])
    n = n_1+n_2 # len(X0[0])+len(X1[0])
    print(m,k,n_1,n_2,n)

    Xp = ( ((n_1-1)*C0) + ((n_2-1)*C1) ) / (n-m)

    M = ((n-m)*np.log(np.linalg.det(Xp))) \
     - (n_1-1)*(np.log(np.linalg.det(C0))) - (n_2-1)*(np.log(np.linalg.det(C1)))

    c = ( ( 2*(k**2) + (3*k) - 1 ) / ( (6*(k+1)*(m-1)) ) ) \
        * ( (1/(n_1-1)) + (1/(n_2-1)) - (1/(n-m)) )

    df = (k*(k+1)*(m-1))/2

    c2 = ( ((k-1)*(k+2)) / (6*(m-1)) ) \
        * ( (1/((n_1-1)**2)) + (1/((n_2-1)**2)) - (1/((n-m)**2)) )

    df2 = (df+2) / (np.abs(c2-c**2))

    if (c2>c**2):

        a_plus = df / (1-c-(df/df2))

        F = M / a_plus

    else:

        a_minus = df2 / (1-c+(2/df2))

        F = (df2*M) / (df*(a_minus-M))

    print('M = {}'.format(M))
    print('c = {}'.format(c))
    print('c2 = {}'.format(c2))
    print('-------------------')
    print('df = {}'.format(df))
    print('df2 = {}'.format(df2))
    print('-------------------')
    print('F = {}'.format(F))
    
def scaleVRF( V : array, u : float, theta : float ) -> array:
    t = 1-theta;
    S = zeros(V.shape);
    S[0,0] = t;
    for i in range(1,S.shape[0]) :
        S[i,0] = S[i-1,0] * t / u;
    for i in range(0,S.shape[0]) :
        for j in range(1,S.shape[1]) :
            S[i,j] = S[i,j-1] * t / u;
    return S * V;
        
if __name__ == '__main__':
    pass
    V = array([[2.0625,1.6875,0.5],[1.6875,    1.75,    0.5625],[0.5,    0.5625,    0.1875]]);

    print(V)
    v = scaleVRF(V, 1e-3, 0.99564)
    print(1.5*sqrt(diag(v)))
    