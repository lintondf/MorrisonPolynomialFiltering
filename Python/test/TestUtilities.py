'''
Created on Feb 15, 2019

@author: NOOK
'''
from math import sin, cos
from numpy import array, diag, ones, zeros
from numpy.random import randn
from scipy.linalg.matfuncs import expm
from scipy.stats import chi2

def stateTransitionMatrix(N : int, dt : float) -> array:
    '''
    Return a Pade' expanded status transition matrix of order m [RMKdR(7)]
        P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= m elsewhere zero
    
    :param N: return matrix is (N,N)
    :param dt: time step
    '''
    B = (diag(ones([N-1]),k=1))
    return expm(dt*B)

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


if __name__ == '__main__':
    pass
    Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
    N = 10;
    order = 1
    tau = 0.1;
    (times, truth, observations, noise) = generateTestData(order, N, 0.0, Y0[0:order+1], tau, sigma=0.0)
    for i in range(0,N) :
        print(times[i], truth[i,:])