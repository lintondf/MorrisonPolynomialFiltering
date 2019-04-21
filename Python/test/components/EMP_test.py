'''
Created on Apr 19, 2019

@author: NOOK
'''

#TODO capture cross section of noise; does it explain variance in variance
import unittest

from copy import deepcopy
from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose
from numpy import sqrt
from numpy.linalg import inv
from numpy.random import randn, seed
from numpy.testing import assert_almost_equal
from numpy.testing.nose_tools.utils import assert_allclose
from numpy.linalg.linalg import norm
from numpy.ma.core import isarray
from scipy.stats import norm as normalDistribution
from math import sin
from runstats import Statistics
# from gevent.libev.corecext import stat

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from polynomialfiltering.Main import AbstractFilterWithCovariance
from polynomialfiltering.components.Emp import makeEmp

class EMP_test(unittest.TestCase):

    Y0 = 0.1*array([1e4, -5e3, +1e3, -5e2, +1e2, -5e1]);


    def setUp(self):
        pass


    def tearDown(self):
        pass
        
    def test0Generate(self):
        for order in range(0,5+1) :
            for tau in (0.01, 0.1, 1, 10) :
                seed(1)
                print(order, tau)
                R = 10.0;
                N = 201
                M = 1000;
                Y = self.Y0;
#                 print('Y0', A2S(Y))
                residuals = zeros([M, N, order+1])
                samples = zeros([M,N])
                for iM in range(0,M) :
                    f = makeEmp(order, tau);
                    (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=R)
                    f.start(0.0, Y)
                    for i in range(0,N) :
                        samples[iM,i] = noise[i];
                        Zstar = f.predict(times[i][0])
                        e = observations[i] - Zstar[0]
                        f.update(times[i][0], Zstar, e)
                        residuals[iM,i,:] = f.getState() - truth[i,:]
        #         print( A2S(residuals[:,400,:]) )
#                 print('Yn', A2S(f.getState()))
                k = 0;
                K = 0 * f.getVRF()
                for j in range(10, N, 10) :
                    f._setN( j );
                    C = cov(residuals[:,j,:],rowvar=False)
                    r = var(samples[:,j])
                    V = r * f.getVRF()
#                     print(j, r)
                    if (order == 0) :
#                         print( A2S( C / V ) )
                        K += C/V;
                    else :
#                         print( A2S( (C) / ( V )) )
                        K += C/V
                    k += 1;
                K = K /k
                print(k, mean(K), (mean(K)-1.0)/R)
#                 print( A2S(K) )
        seed()

    def xtest0Generate(self):
        order = 5
        tau = 0.1
        R = 10.0;
        N = 500
        f = makeEmp(order, tau);
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
        f.start(0.0, self.Y0[0:order+1])
        residuals = zeros([N, order+1]);
        for i in range(0,N) :
            Zstar = f.predict(times[i][0])
            e = observations[i] - Zstar[0]
            f.update(times[i][0], Zstar, e)
            V = f.getVRF();
            if (V[0,0] > 0 and V[1,1] <= 1) :
                break;
        print(i,diag(V))
        for i in range(i+1,i+3) :
            print(i,A2S(diag(V)))
            empP1 = deepcopy(f)
            empM1 = deepcopy(f)
#             k = -0.5
#             n = 1.0
#             w0 = k/(n+k)
#             wi = R/(2*(n+k))
#             s = sqrt(n+k)
#         A = wi * array([-s, +s])
#         O = array([-s, +s]);
#             print(i, wi*(O @ O.T))
#             k = 0.5;
#             a = 0.5;
#             b = 2;
#             g = 1; # a*a*(1+k)-1
#             wm = g/(1+g)
#             wc = wm# + (1-a*a+b)
            s = R
            wc = 0.5
            e0 = observations[i] - Zstar[0]
            em1 = (observations[i] - s) - Zstar[0]
            ep1 = (observations[i] + s) - Zstar[0]
            f.update(times[i][0], Zstar, e0)
            y0 = f.getState()
            V = f.getVRF();
            empP1.update(times[i][0], Zstar, em1)
            ym1 = empP1.getState()
            empM1.update(times[i][0], Zstar, ep1)
            yp1 = empM1.getState()
            
#             print('y 0', A2S(y0))
#             print('y-1', A2S(ym1))
#             print('y+1', A2S(yp1))
            
            zm1 = (ym1 - y0);
            zm1.shape = (order+1,1)
            zp1 = (yp1 - y0);
            zp1.shape = (order+1,1)
    #         print(A2S(zm1), A2S(zp1))
            C = wc*(zm1 @ zm1.T)
            C += wc*(zp1 @ zp1.T)
            print(i, A2S(diag(C)))
            r = C / (R*R*V)
            print('C/V', A2S(diag(r)))
                
        
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()