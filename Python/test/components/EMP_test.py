'''
Created on Apr 19, 2019

@author: NOOK
'''

#TODO capture cross section of noise; does it explain variance in variance
import unittest

from copy import deepcopy
from TestUtilities import *
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where
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
        
    def xtestVerifyVRFExtended(self):
        for i in range(0,25) :
            self.doVerifyVRF()
    
    def xtestVerifyVRF(self):
        self.doVerifyVRF();
        
    def doVerifyVRF(self):
        for order in range(0, 5+1) :
            for tau in (0.01, 0.1, 1, 10) :
#                 seed(1)
                R = 10.0 * tau;
                N = 1001
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
                    if (f.getLastVRF() < 1.0) :
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
                dFirst = nonzero(distances)
                dFirst = dFirst[0]
                if (len(dFirst) == 0) :
                    dFirst = 0;
                else :
                    dFirst = dFirst[0]
                    dFirst = int(dFirst)
                fit = lognorm.fit(distances[dFirst:], fscale=1) # fit only sigma and mean
                print('%1d, %6.2f, %6.2f, %6.2f, %10.3f, %10.3f, %10.3f,  %10.3f, %10.3f' % ( order, tau,\
                    100*(min(diag(K))-1.0), 100*(mean(diag(K))-1.0), 100*(max(diag(K))-1.0), \
                    100*mean(distances[dFirst:]), 100*std(distances[dFirst:]), fit[0], fit[1] ))
#                 f = Fitter(distances[order+1:])
#                 f.verbose = False;
#                 f.distributions = ['loggamma', 'chi2', 'norm', 'lognorm']
#                 f.fit()
#                 print(f.summary())
#                 print(f.get_best())
                
#                 num_bins = 50
#                 n, bins, patches = plt.hist(100*distances[order+1:], num_bins, facecolor='blue', alpha=0.5)
#                 print(A2S(distances))
#                 f0 = plt.figure(figsize=(10, 6))
#                 ax = plt.subplot(1, 1, 1)
#                 ax.plot(range(dFirst,N), 100*distances[dFirst:], 'k-')
#                 plt.show()
        seed()
        
    def driver(self, order : int, tau : float):
#         seed(1)
        R = 1.0 * tau;
        N = 501
        Y = self.Y0 / tau;
        actual = zeros([N,order+1]);
        schi2 = zeros([N,4])
        f = makeEmp(order, tau);
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, Y[0:order+1], tau, sigma=R)
        print(mean(noise), std(noise), R)
        f.start(0.0, Y)
        iFirst = 0;
        for i in range(0,N) :
            Zstar = f.predict(times[i][0])
            e = observations[i] - Zstar[0]
            f.update(times[i][0], Zstar, e)
            if (f.getStatus() == FilterStatus.RUNNING) :
                if (iFirst == 0) :
                    iFirst = i;
                actual[i,:] = f.getState()
                r = f.getState() - truth[i,:]
#                 R = var(noise[0:i+1])
                V = R**2 * f.getVRF();
                schi2[i, 0] = r[0]**2 / V[0,0] # r @ inv(V) @ transpose(r)
                schi2[i, 1] = V[0, 0]
                schi2[i, 2] = r[0]**2
                schi2[i, 3] = mean(observations[0:i+1])
#                 print('%5d, %10.6f, %10.6f, %10.6f, %10.6f' % (i, schi2[i,0], schi2[i,1], schi2[i,2], schi2[i,3]))
#                 print(schi2[i,:], chi2.cdf(schi2[i,:], df=1))
#                 schi2[i, 1:order+2] = r / sqrt(diag(V));
#                 if ((i % 10) == 0) : 
#                     print( '%5d %s' % (i, A2S(schi2[i,:])) )
#         f = Fitter(schi2[iFirst:,0])
#         f.verbose = False;
#         f.distributions = ['loggamma', 'chi2', 'norm', 'lognorm']
#         f.fit()
#         print(f.summary())
#         print(f.get_best())
#         fit = chi2.fit(schi2[iFirst:,0], fscale=1) # fit only sigma and mean
#         print('%5d, %6.3f, %10.3f, %10.3f, %10.3f, %10.6f, %10.6f, %10.6f' % (order, tau,  100*min(schi2[iFirst:,0]), 100*mean(schi2[iFirst:,0]), 100*max(schi2[iFirst:,0]), fit[0], fit[1], fit[2]))
        threshold = chi2.ppf(array([0.95, 0.96]),df=1);
#         bin_values = chi2.ppf(array([0.5, 0.75, 0.9, 0.95, 0.99, 0.9999999999]), df=1)
#         n, bins, patches = plt.hist(schi2[iFirst:,0], bin_values, facecolor='blue', alpha=0.5)
#         plt.show()
#         n, __ = histogram(schi2[iFirst:,0], bin_values);
#         cn = cumsum(n/sum(n));
#         return cn[3]
#         print(cn, cn[3]-0.95)
#         C = cov(schi2, rowvar=False);
#         (s, Q) = covarianceToCorrelation(C)
#         print(A2S(s))
#         print( A2S( Q ))
#         return mean(schi2[:,0])
#         print(A2S(schi2[iFirst:,0]))
#         print(A2S(threshold))
#         print(where(schi2[iFirst:,0] > threshold[0]))
        n95 = len(where(schi2[iFirst:,0] < threshold[0])[0])/(N-iFirst)
        n96 = len(where(schi2[iFirst:,0] < threshold[1])[0])/(N-iFirst)
        if (n95 < 0.95) :
            print(A2S(schi2))
            print(order, tau, n95, n96)
            f0 = plt.figure(figsize=(10, 6))
            ax = plt.subplot(1, 1, 1)
            ax.plot(array([0,N]), array([threshold[0], threshold[0]]), 'r-')
            ax.plot(range(iFirst,N), schi2[iFirst:,0], 'k-', range(iFirst,N), schi2[iFirst:,1], 'b.')
            f0 = plt.figure(figsize=(10, 6))
            ax = plt.subplot(1, 1, 1)
            ax.plot(times[iFirst:N,0], actual[iFirst:N,0], 'k-', times[iFirst:N,0], observations[iFirst:N], 'b.', times[iFirst:N,0], truth[iFirst:N,0], 'r-')
            f0 = plt.figure(figsize=(10, 6))
            ax = plt.subplot(1, 1, 1)
            ax.plot(arange(iFirst,N,1), schi2[iFirst:,1], 'k.', arange(iFirst,N,1), schi2[iFirst:,2], 'b.')
            plt.show()
        return (n95, n96)

    def test0Generate(self):
        for order in range(0, 5+1) :
            for tau in [1] : #[0.01, 0.1, 1, 10] :
                c9596 = zeros([25,2])
                for j in range(0,c9596.shape[0]) :
                    n95, n96 = self.driver(order, tau )
                    c9596[j,:] = [n95, n96]
                ci = mean(c9596,axis=0)+std(c9596,axis=0);
                print('%3d, %6.3f, %6.4f, %6.4f' % (order, tau, mean(c9596[:,0]), max(c9596[:,0]) ))
#                     if (n95 > 0.05 and n96 > 0.04) :
#                         print(order, tau, j, n95, n96)
#                 print('%3d, %6.3f, %6.4f, %6.4f, %6.4f, %6.4f' % (order, tau, min(c95), max(c95), mean(c95), mean(c95)-std(c95)))
#                 print( fsolve(lambda x: self.driver(order, tau, x), 0.0) )
#                 for dt in arange(-0.0, 1, 0.1) :
#                     print(dt, self.driver(order, tau, dt))
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