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
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag
from numpy import sqrt
from numpy.linalg import inv
from numpy.random import randn, seed, get_state
from numpy.testing import assert_almost_equal
from scipy.stats import kstest, chi2, lognorm, norm, anderson

from runstats import Statistics

from netCDF4 import Dataset
from TestSuite import testDataPath;
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S
from TestData import TestData

from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.components.Emp import makeEmp, makeEmpCore, nUnitLastVRF

from polynomialfiltering.PythonUtilities import ignore, testcase
from polynomialfiltering.PythonUtilities import assert_not_empty


class RecursivePolynomialFilterMock(RecursivePolynomialFilter):
    
    def __init__(self, order : int, tau : float, core : ICore):
        super().__init__(order, tau, core)
        
    def setN(self, n : int) -> int:
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


    def oneCrossSectionChi2(self, order : int, N : array, M : array, R : float) -> List[List[Statistics]]:
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
    
    def crossSectionChi2(self, mScale : int = 16) -> None:
        R = 10.0
        N = array([64, 128, 128, 256, 512, 1024])
        M = mScale*array([8, 8, 8, 8, 8, 8])
        for order in range(0, 5+1) :
            print(order, N[order], M[order])
            stats = self.oneCrossSectionChi2( order, N, M, R );
            for k1 in range(0,order+1) :
                for k2 in range(0,order+1) :
                    print('%6.4f, ' % (stats[k1][k2].mean()+stats[k1][k2].stddev()), end='')
                print('')
            print('')
             
    def fastCrossSectionChi2(self) -> None:
        # seed 1, small sample values values
        expected = [
            array([[0.8419]]),
            array([[1.1991, 1.4528], 
                   [1.4528, 1.4643]]),
            array([[1.3971, 1.5505, 1.6142], 
                   [1.5505, 1.5338, 1.5313], 
                   [1.6142, 1.5313, 1.4946]]),
            array([[1.2169, 1.3142, 1.3830, 1.4468], 
                   [1.3142, 1.4103, 1.4693, 1.5117], 
                   [1.3830, 1.4693, 1.5217, 1.5577], 
                   [1.4468, 1.5117, 1.5577, 1.5901]]),
            array([[1.2824, 1.3594, 1.4138, 1.4605, 1.5023], 
                   [1.3594, 1.3669, 1.3936, 1.4203, 1.4470], 
                   [1.4138, 1.3936, 1.4118, 1.4331, 1.4553], 
                   [1.4605, 1.4203, 1.4331, 1.4509, 1.4701], 
                   [1.5023, 1.4470, 1.4553, 1.4701, 1.4867]]),
            array([[1.3341, 1.3766, 1.4271, 1.4773, 1.5248, 1.5701], 
                   [1.3766, 1.3646, 1.3881, 1.4120, 1.4343, 1.4557], 
                   [1.4271, 1.3881, 1.4036, 1.4213, 1.4374, 1.4523], 
                   [1.4773, 1.4120, 1.4213, 1.4354, 1.4486, 1.4607], 
                   [1.5248, 1.4343, 1.4374, 1.4486, 1.4598, 1.4702], 
                   [1.5701, 1.4557, 1.4523, 1.4607, 1.4702, 1.4795]]),
            ]
        seed(1)
        R = 10.0
        N = array([64, 128, 128, 256, 512, 1024])
        M = array([8, 8, 8, 8, 8, 8])
        for order in range(0, 5+1) :
            stats = self.oneCrossSectionChi2( order, N, M, R );
            for k1 in range(0,order+1) :
                for k2 in range(0,order+1) :
                    actual = stats[k1][k2].mean()+stats[k1][k2].stddev();
                    assert_almost_equal(actual, expected[order][k1][k2], decimal=4)
        seed()
    
    def generateVRF(self, cdf : Dataset) -> None:
        for order in range(0,5+1) :
            group = createTestGroup(cdf, 'VRF_%d' % order );
            setup = array([500])
            writeTestVariable(group, "setup", setup);
            N = setup[0]
            taus = array([0.01, 0.1, 1, 10])
            writeTestVariable(group, "taus", taus);
            expected = zeros([0, order+1]);
            for itau in range(0,len(taus)) :
                tau = taus[itau]
                core = makeEmpCore(order, tau)
                f = RecursivePolynomialFilterMock( order, tau, core )
                for iN in range(order+1, N) :
                    f.setN(iN)
                    expected = concatenate([expected, f.getVRF()]);
            writeTestVariable(group, "expected", expected)
            

    
    def generateStates(self, cdf : Dataset) -> None:
        print("generateStates", chi2.ppf(0.95,df=1))
        R = 10.0
        N = array([64, 128, 512, 512, 1024, 2048])
        setup = array([
            [0, 0.01],[0, 0.1], [0, 1.0], [0, 10.0],  
            [1, 0.01],[1, 0.1], [1, 1.0], [1, 10.0],  
            [2, 0.01], [2, 0.1], [2, 1.0], [2, 10.0],  
            [3, 0.01], [3, 0.1], [3, 1.0], [3, 10.0],  
            [4, 0.01],[4, 0.1], [4, 1.0], [4, 10.0],  
            [5, 0.01],[5, 0.1], [5, 1.0], [5, 10.0]
            ])
        group = createTestGroup(cdf, 'States')
        writeTestVariable(group, 'setup', setup)
        for i in range(0,setup.shape[0]) :
            order = int(setup[i,0])
            tau = setup[i,1]
            case = createTestGroup(cdf, 'Case_%d' % i)
            t0 = 0.0
            Y = generateTestPolynomial( order, N[order], t0, tau )
            for retry in range(0,10) :
                (times, truth, observations, noise) = generateTestData(order, N[order], 0.0, Y[0:order+1], tau, sigma=R)
    
                expected = zeros([N[order], order+1])            
                f = makeEmp(order, tau);
                f.start(0.0, Y)
                iGood = 0;
                iBad = 0;
                tchi2 = chi2.ppf(0.95, df=order+1)
                for j in range(0,times.shape[0]) :
                    Zstar = f.predict(times[j][0])
                    e = observations[j] - Zstar[0]
                    f.update(times[j][0], Zstar, e)
                    expected[j,:] = f.getState();
                    if (f.getStatus() == FilterStatus.RUNNING and f.getFirstVRF() < 1.0 ) : # R**2 * f.getLastVRF() < 1.0) :                
                        V = f.getVRF()
                        V *= R**2;
                        error = f.getState() - truth[j,:] # f.getState()[0] - truth[j,0]
                        testChi2 = transpose(error) @ inv(V) @ (error) # error**2 / V[0,0] # 
                        if (testChi2 > tchi2) :
    #                         print(order, tau, j, testChi2)
    #                         print(A2S(error))
    #                         print(A2S(V))
                            iBad += 1
                        else :
                            iGood += 1;
                if (iBad / (iBad+iGood) < 0.05) :
                    break;
            assert(retry < 10)
            print('%5d, %6.3f, %3d, %6.3f' % (order, tau, retry, iBad / (iBad+iGood) ))
            writeTestVariable(case, 'times', times)
            writeTestVariable(case, 'observations', observations)
            writeTestVariable(case, 'expected', expected)
       
    def test0Generate(self):
        print("test0Generate")
        path = testDataPath('testEMP.nc');
        cdf = Dataset(path, "w", format="NETCDF4");
        self.generateVRF(cdf)
        self.generateStates(cdf)
        cdf.close()
       
    @testcase        
    def test1CheckVRF(self) -> None:
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@i : int'''
        print("test1CheckVRF")
        testData = TestData('testEMP.nc')
        matches = testData.getMatchingGroups('VRF_')
        assert_not_empty(matches)
        for order in range(0, len(matches)) :
            setup = testData.getGroupVariable(matches[order], 'setup')
            N = int(setup[0,0])            
            taus = testData.getGroupVariable(matches[order], 'taus')
            expected = testData.getGroupVariable(matches[order], 'expected')
            offset = 0;
            for itau in range(0,len(taus)) :
                tau = taus[itau,0]
                core = makeEmpCore(order, tau)
                f = RecursivePolynomialFilterMock( order, tau, core )
                for iN in range(order+1, N) :
                    f.setN(iN)
                    V = f.getVRF();
                    assert_almost_equal(V, expected[offset:offset+order+1,:])
                    offset += order+1
                    assert_almost_equal(V[0,0], f.getFirstVRF())
                    assert_almost_equal(V[-1,-1], f.getLastVRF())
                    assert_almost_equal(diag(V), diag(f.getDiagonalVRF()))
                
    @testcase
    def test2CheckStates(self) -> None:
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@i : int'''
        print("test2CheckStates")
        testData = TestData('testEMP.nc')
        matches = testData.getMatchingGroups('States')
        assert_not_empty(matches)
        setup = testData.getGroupVariable(matches[0], 'setup')
        matches = testData.getMatchingGroups('Case_')
        assert_not_empty(matches)
        for i in range(0, len(matches)) :
            order = int(setup[i,0])
            tau = setup[i,1]
            print(matches[i], order, tau)
            times = testData.getGroupVariable(matches[i], 'times')
            observations = testData.getGroupVariable(matches[i], 'observations')
            expected = testData.getGroupVariable(matches[i], 'expected')
            actual = zeros(expected.shape)            
            f = makeEmp(order, tau);
            f.start(0.0, expected[0,:])
            for j in range(0,times.shape[0]) :
                Zstar = f.predict(times[j][0])
                e = observations[j] - Zstar[0]
                f.update(times[j][0], Zstar, e)
                actual[j,:] = f.getState();
            diff = actual-expected
            assert_almost_equal(actual, expected)
        
    def test9CrossSectionChi2(self):
        print("test9CrossSectionChi2")
        if (slow()) :
            self.crossSectionChi2()
        else :
            self.fastCrossSectionChi2()


           
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()