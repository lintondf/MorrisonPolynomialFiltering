'''
Created on Apr 19, 2019

@author: NOOK
'''

#TODO capture cross section of noise; does it explain variance in variance
import unittest
from typing import List;

from TestSuite import slow

from numpy import array, array as vector
from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose,\
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where
from numpy import sqrt
from numpy.linalg import inv
from numpy.random import randn, seed, get_state
from numpy.testing import assert_almost_equal
from scipy.stats import kstest, chi2, lognorm, norm, anderson

from runstats import Statistics

from TestUtilities import generateTestPolynomial, generateTestData
from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.components.Emp import makeEmp, makeEmpCore, nUnitLastVRF
from polynomialfiltering.PythonUtilities import ignore

class RecursivePolynomialFilterMock(RecursivePolynomialFilter):
    
    def __init__(self, order : int, tau : float, core : ICore):
        super().__init__(order, tau, core)
        
    def setN(self, n : int):
        self.n = n;
        

class EMP_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def driver(self, order : int, tau : float, N : int, R : float = 10.0):
#         state = get_state()
#         print(state)
#         seed(1)
        t0 = 0.0
        Y = generateTestPolynomial( order, N, t0, tau )
        errors = zeros([N,order+1]);
        schi2 = zeros([N,4])
        f = makeEmp(order, tau);
        (times, truth, observations, noise) = generateTestData(order, N, 0.0, Y[0:order+1], tau, sigma=R)
#         print('%5d, %6.3f, %10.3f, %10.3f' % (order, tau,  mean(noise**2), var(noise**2)))
        f.start(0.0, Y)
        iFirst = 0;
        for i in range(0,N) :
            Zstar = f.predict(times[i][0])
            V = f.getVRF()
            e = observations[i] - Zstar[0]
            f.update(times[i][0], Zstar, e)
            if (f.getStatus() == FilterStatus.RUNNING) :
                if (iFirst == 0 and f.getFirstVRF() < 1.0) :
                    iFirst = i;
                error = f.getState() - truth[i,:]
#                 if ( i == 63) :
#                     print(i, error)
                errors[i,:] = error
                V = f.getVRF()
                V *= R**2;
                schi2[i, 0] = error @ inv(V) @ transpose(error)
                schi2[i, 1] = V[0,0]
                schi2[i, 2] = error[0]
                schi2[i, 3] = var(noise[0:i+1])
                
#         print(kstest(schi2[:, 0]**2, lambda x: chi2.cdf(x,df=1),alternative='greater'))
#                 print('%5d, %10.6f, %10.6f, %10.6f, %10.6f, %10.6f' % (i, schi2[i,0], schi2[i,1], schi2[i,2], schi2[i,3], noise[i]))
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
#         print('%5d, %6.3f, %10.3f, %10.3f' % (order, tau,  mean(schi2[iFirst:,0]), var(schi2[iFirst:,0])))
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
#         print( jarque_bera(schi2[iFirst:,2]/sqrt(schi2[iFirst:,3])) )#  # noise/R
        threshold = chi2.ppf(array([0.95, 0.99]),df=order+1);
        n95 = len(where(schi2[iFirst:,0] > threshold[0])[0])
        return (n95, errors)
#             print(threshold)
#             print(A2S(chi2.cdf(schi2[where(schi2[:,0] > threshold[0])[0],0],df=order+1)) )
#             print(A2S(schi2))
#             print('%3d, %6.3f, %6.4f, %6.4f  FAIL' % (order, tau, n95, n96))
#             f0 = plt.figure(figsize=(10, 6))
#             ax = plt.subplot(1, 1, 1)
#             ax.plot(array([0,N]), array([threshold[0], threshold[0]]), 'r-', label='95%')
#             ax.plot(range(iFirst,N), schi2[iFirst:,0], 'k-', label='Chi2')
#             ax.legend()
#             f0 = plt.figure(figsize=(10, 6))
#             ax = plt.subplot(1, 1, 1)
#             ax.plot(range(iFirst,N), +sqrt(schi2[iFirst:,1]), 'm-', label='V[0,0]')
#             ax.plot(range(iFirst,N), -sqrt(schi2[iFirst:,1]), 'm-', label='V[0,0]')
#             ax.plot(range(iFirst,N), schi2[iFirst:,2], 'b.', label='error')
#             ax.plot(range(iFirst,N), noise[iFirst:], 'r.', label='noise')
#             ax.legend()
#             f0 = plt.figure(figsize=(10, 6))
#             ax = plt.subplot(1, 1, 1)
#             ax.plot(times[iFirst:N,0], actual[iFirst:N,0], 'k-', times[iFirst:N,0], observations[iFirst:N], 'b.', times[iFirst:N,0], truth[iFirst:N,0], 'r-')
#             f0 = plt.figure(figsize=(10, 6))
#             ax = plt.subplot(1, 1, 1)
#             ax.plot(arange(iFirst,N,1), schi2[iFirst:,1], 'k.', arange(iFirst,N,1), schi2[iFirst:,2], 'b.')
#             plt.show()


    @ignore
    def oneCrossSectionChi2(self, order : int, N : array, M : array, R : float) -> List[List[Statistics]]:
        print(order, N[order], M[order])
        stats = [[Statistics() for j in range(order+1)] for i in range(order+1)]
        for tau in [0.01, 0.1, 1, 10] :
            E = zeros([N[order], M[order], order+1])
            for iM in range(0, M[order]) :
                errors = self.driver(order, tau, N[order], R )[1]
                E[:, iM,:] = errors
                
#                 f = makeEmp(order, tau);
            core = makeEmpCore(order, tau)
            f = RecursivePolynomialFilterMock( order, tau, core )
            for iN in range(0, N[order]) :
                f.setN(iN)
                if (iN > order+1 and f.getFirstVRF() > 0 and f.getFirstVRF() < 1.0) :
                    X = cov(E[iN,:,:],rowvar=False)
                    V = R**2 * f.getVRF()
                    XV = X / V
                    for k1 in range(0,order+1) :
                        for k2 in range(0,order+1) :
                            stats[k1][k2].push(XV[k1,k2]);
        return stats;
    
    #ignore
    def crossSectionChi2(self, mScale : int = 16) -> None:
        R = 10.0
        N = array([64, 128, 128, 256, 512, 1024])
        M = mScale*array([8, 8, 8, 8, 8, 8])
#         bin_values = chi2.ppf(array([0.0, 0.5, 0.75, 0.9, 0.95, 0.99, 0.9999999999]), df=1)
        for order in range(0, 5+1) :
            stats = self.oneCrossSectionChi2( order, N, M, R );
            for k1 in range(0,order+1) :
                for k2 in range(0,order+1) :
                    print('%6.4f, ' % (stats[k1][k2].mean()+stats[k1][k2].stddev()), end='')
                print('')
            print('')
             
    def generateVRF(self) -> None:
        pass
    
    def generateStates(self) -> None:
        pass
       
    def test0CrossSectionChi2(self):
        print("test0CrossSectionChi2")
        if (slow()) :
            self.crossSectionChi2()
        else :
            seed(1)
            self.crossSectionChi2(1)
            seed()
            

    def test0Generate(self):
        print("test0Generate")
        self.generateVRF()
        

           
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()