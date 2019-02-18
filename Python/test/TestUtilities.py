'''
Created on Feb 15, 2019

@author: NOOK
'''
from math import sin, cos
import numpy as np
from numpy import array, array2string, diag, eye, ones, zeros
from numpy.random import randn
from scipy.linalg.matfuncs import expm
from scipy.stats import chi2

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
    B = eye(N)
    for i in range(0,N) :
        for j in range(i+1,N):
            ji = j-i
            fji = ji
            for x in range(2,ji) :
                fji *= x 
            B[i,j] = pow(dt,ji)/fji
    return B

def generateTestData(order, N, t0, Y0, dt, bias=0.0, sigma=1.0):
    if (order >= 0) :
        truth = zeros([N,order+1])
        noise = bias + sigma*randn(N,1)
        observations = zeros([N])
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
     
if __name__ == '__main__':
    pass
    box_m(5000, np.cov(randn(2,5000)), 400000, np.eye(2,2))
#     Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
#     N = 10;
#     order = 1
#     tau = 0.1;
#     (times, truth, observations, noise) = generateTestData(order, N, 0.0, Y0[0:order+1], tau, sigma=0.0)
#     for i in range(0,N) :
#         print(times[i], truth[i,:])