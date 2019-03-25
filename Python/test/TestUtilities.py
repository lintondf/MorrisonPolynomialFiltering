'''
Created on Feb 15, 2019

@author: NOOK
'''

import time
from typing import Tuple;
from netCDF4 import Dataset
from math import sin, cos, exp
import numpy as np
from numpy import array, array2string, diag, eye, ones, transpose, zeros, sqrt, mean, std, var
from numpy import array as vector
from numpy.linalg.linalg import det, inv
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
    
def hellingerDistance( u1, P1, u2, P2 ):
    P12 = 0.5 * (P1 + P2)
    a = det(P1)**0.25 * det(P2)**0.25 / det(P12)**0.5;
    b = -(1/8)* transpose(u1-u2) @ inv(P12) @ (u1-u2)
#     print(det(P1), det(P2), det(P12), a, b)
    return sqrt(1 - a * exp(b));

def covarianceIntersection( P1, P2 ):
    I1 = inv(P1)
    I2 = inv(P2)
    dI1 = det(I1)
    dI2 = det(I2)
    dI12 = det(I1+I2)
    w1 = (dI12 - dI2 + dI1) / (2*dI12);
    w2 = 1 - w1;
    P = inv( w1 * I1 + w2 * I2);
    print('w1 = ', w1)
    return P

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
        Y = zeros([order+1]);
        m = min( order+1, len(Y0) )
        Y[0:m] = Y0[0:m];
        for i in range(0,N) :
            times[i] = t
            m = min( truth.shape[1], len(Y) )
            truth[i,0:m] = Y[0:m]
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

def correlationToCovariance( R : array, d : vector ) -> array:
    D = diag( d );
    return D @ R @ D;

def covarianceToCorrelation( C : array ) -> Tuple[array, vector]:
    d = sqrt(diag(C));
    D = diag( 1. / d )
    return (D @ C @ D, d); 

def nearPSD(A,epsilon=0):
    n = A.shape[0]
    eigval, eigvec = np.linalg.eig(A)
    val = np.matrix(np.maximum(eigval,epsilon))
    vec = np.matrix(eigvec)
    T = 1/(np.multiply(vec,vec) * val.T)
    T = np.matrix(np.sqrt(np.diag(np.array(T).reshape((n)) )))
    B = T * vec * np.diag(np.array(np.sqrt(val)).reshape((n)))
    out = B*B.T
    return(out)

def _getAplus(A):
    eigval, eigvec = np.linalg.eig(A)
    Q = np.matrix(eigvec)
    xdiag = np.matrix(np.diag(np.maximum(eigval, 0)))
    return Q*xdiag*Q.T

def _getPs(A, W=None):
    W05 = np.matrix(W**.5)
    return  W05.I * _getAplus(W05 * A * W05) * W05.I

def _getPu(A, W=None):
    Aret = np.array(A.copy())
    Aret[W > 0] = np.array(W)[W > 0]
    return np.matrix(Aret)

def nearPD(A, nit=10):
    n = A.shape[0]
    W = np.identity(n) 
# W is the matrix used for the norm (assumed to be Identity matrix here)
# the algorithm should work for any diagonal W
    deltaS = 0
    Yk = A.copy()
    for k in range(nit):
        Rk = Yk - deltaS
        Xk = _getPs(Rk, W=W)
        deltaS = Xk - Rk
        Yk = _getPu(Xk, W=W)
    return Yk

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
    
def scaleVRFFMP( V : array, u : float, theta : float ) -> array:
    t = 1-theta;
    S = zeros(V.shape);
    S[0,0] = t;
    for i in range(1,S.shape[0]) :
        S[i,0] = S[i-1,0] * t / u;
    for i in range(0,S.shape[0]) :
        for j in range(1,S.shape[1]) :
            S[i,j] = S[i,j-1] * t / u;
    return S * V;
        
def scaleVRFEMP( V : array, t : float, n : float ) -> array:
    '''@S : array'''
    '''@i : int'''
    '''@j : int'''
    S = zeros([V.shape[0], V.shape[1]]);
    S[0,0] = 1.0/n;
    for i in range(1,S.shape[0]) :
        S[i,0] = S[i-1,0] / (t*n);
    for i in range(0,S.shape[0]) :
        for j in range(1,S.shape[1]) :
            S[i,j] = S[i,j-1] / (t*n);
    return S * V;
        
            
if __name__ == '__main__':
    pass
    N = randn(10,1)
    print(mean(N), std(N))
    N2 = N*N;
    print(mean(chi2.cdf(N2,1)))
    print(chi2.cdf(sum(N2)/len(N2),len(N2)))
    
        
    