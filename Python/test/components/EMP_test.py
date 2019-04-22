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
from fitter import Fitter


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab

from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.components.Emp import makeEmp, makeEmpCore
from scipy.stats import kstest, chi2, lognorm
from scipy.optimize import fsolve

class EMP_test(unittest.TestCase):

    Y0 = array([1e3, -5e2, +1e2, -5e0, +1e0, -5e-1]);


    def setUp(self):
        pass


    def tearDown(self):
        pass
        
    def testVerifyVRF(self):
        for i in range(0,25) :
            self.doVerifyVRF()
            
    def doVerifyVRF(self):
        for order in range(0,5+1) :
            for tau in (0.01, 0.1, 1, 10) :
#                 seed(1)
                R = 10.0 * tau;
                N = 401
                M = 500;
                Y = self.Y0 / tau;
#                 print('Y0', A2S(Y))
                residuals = zeros([M, N, order+1])
                samples = zeros([M,N])
                distances = zeros([N,1]);
                for iM in range(0,M) :
                    f = makeEmp(order, tau);
                    (times, truth, observations, noise) = generateTestData(order, N, 0.0, Y[0:order+1], tau, sigma=R)
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
                for j in range(order+1, N) :
                    f._setN( j );
                    C = cov(residuals[:,j,:],rowvar=False)
                    uC = mean(residuals[:,j,:], axis=0)
                    r = var(samples[:,j])
                    V = r * f.getVRF()
                    distances[j] = hellingerDistance(uC, C, 0*uC, V);
                    if (j > 50) :
                        if (order == 0) :
                            K += C/V;
                        else :
                            K += C/V
                        k += 1;
                K = K /k
                fit = lognorm.fit(distances[order+1:], fscale=1) # fit only sigma and mean
                print('%1d, %6.2f, %10.3f, %10.3f, %10.3f,  %10.3f, %10.3f' % ( order, tau, 100*(mean(K)-1.0), \
                    100*mean(distances[order+1:]), 100*std(distances[order+1:]), fit[0], fit[1] ))
#                 f = Fitter(distances[order+1:])
#                 f.verbose = False;
#                 f.distributions = ['loggamma', 'chi2', 'norm', 'lognorm']
#                 f.fit()
#                 print(f.summary())
#                 print(f.get_best())
                
#                 num_bins = 50
#                 n, bins, patches = plt.hist(100*distances[order+1:], num_bins, facecolor='blue', alpha=0.5)
#                 plt.show()
        seed()
        
    def driver(self, order : int, tau : float, dt : float):
        seed(1)
        R = 10.0;
        N = 1501
        Y = self.Y0;
        schi2 = zeros([N,4])
        f = makeEmp(order, tau);
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=R)
        f.start(0.0, Y)
        for i in range(0,N) :
            Zstar = f.predict(times[i][0])
            e = observations[i] - Zstar[0]
            f.update(times[i][0], Zstar, e)
            if (f.getStatus() == FilterStatus.RUNNING) :
                r = f.getState() - truth[i,:]
                V = R**2 * f.getVRF();
                V = AbstractFilterWithCovariance.transitionCovarianceMatrix(dt, V)
                schi2[i, 0] = r @ inv(V) @ transpose(r)
                schi2[i, 1:order+2] = r / sqrt(diag(V));
#                         if ((i % 10) == 0) : 
#                             print( '%5d %s' % (i, A2S(schi2[i,:])) )
        return mean(schi2[:,1])

    def xtest0Generate(self):
        for order in range(2,2+1) :
            for tau in [0.1] : #[0.01, 0.1, 1, 10] :
#                 print( fsolve(lambda x: self.driver(order, tau, x), 0.0) )
                for dt in arange(-0.0, 1, 0.1) :
                    print(dt, self.driver(order, tau, dt))
#                 print(order, tau)
#                 print(kstest(schi2[1000:,0], lambda x: chi2.cdf(x, df=order+1)));
#                 print(kstest(schi2[1000:,1], 'norm' ))
#                 print(kstest(schi2[1000:,2], 'norm' ))
#                 print(kstest(schi2[1000:,3], 'norm' ))
#                 num_bins = 50
#                 n, bins, patches = plt.hist(schi2[:,1], num_bins, facecolor='blue', alpha=0.5)
#                 plt.show()
                        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()