'''
Created on Sep 16, 2019

@author: lintondf
'''
import unittest

from numpy import arange, array2string, cov, log, var, zeros, trace, mean, std, transpose, \
    concatenate, allclose, min, max, nonzero, cumsum, histogram, where, diag, ones
from numpy import array, array as vector, array_equal
from numpy import sqrt
from TestUtilities import assert_allclose, assert_almost_equal, assert_array_less
from scipy.optimize.zeros import brentq
from typing import List;

from TestData import TestData
from TestSuite import slow, TestCaseBase
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S, assert_report, assert_clear
from polynomialfiltering.Main import AbstractFilterWithCovariance, FilterStatus
from polynomialfiltering.PythonUtilities import assert_not_empty
from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.components.Emp import nSwitch
from polynomialfiltering.components.ICore import ICore
from polynomialfiltering.filters.PairedPolynomialFilter import PairedPolynomialFilter
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter


# from numpy.linalg import inv
# from numpy.random import randn, seed, get_state
# from scipy.stats import kstest, chi2, lognorm, norm, anderson
# from runstats import Statistics
# from netCDF4 import Dataset
# from TestSuite import testDataPath;
class Pair_test(TestCaseBase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def thetaFromN(self, order : int, n : int )-> float :
        def targetTheta(theta : float) -> float:
            return  n - nSwitch(order, theta)
        
        t0 = brentq( targetTheta, 1e-6, 1-1e-8 );
        return t0


    def generateStates(self, testData : TestData) -> None:
        R = 10.0
        N = array([64, 128, 512, 512, 1024, 2048])
        thetas = array([0.9375, 0.95, 0.978494296875, 0.9829546875, 0.9870466796875, 0.9924337890625])
        setup = array([
            [0, 0.01],[0, 0.1], [0, 1.0], [0, 10.0],  
            [1, 0.01],[1, 0.1], [1, 1.0], [1, 10.0],  
            [2, 0.01], [2, 0.1], [2, 1.0], [2, 10.0],  
            [3, 0.01], [3, 0.1], [3, 1.0], [3, 10.0],  
            [4, 0.01],[4, 0.1], [4, 1.0], [4, 10.0],  
            [5, 0.01],[5, 0.1], [5, 1.0], [5, 10.0]
            ])
        group = testData.createTestGroup('States')
        for i in range(0,setup.shape[0]) :
            case = testData.createTestGroup( 'States_Case_%d' % i)
            order = int(setup[i,0])
            tau = setup[i,1]
            theta = self.thetaFromN( order, N[order]//2)  # thetas[i]
            nS = int(nSwitch( order, theta ))
            testData.putInteger(case, 'order', order)
            testData.putScalar(case, 'tau', tau)
            testData.putScalar(case, 'theta', theta)
            testData.putInteger(case, 'nS', nS)
            testData.putInteger(case, 'N', N[order])
            t0 = 0.0
            Y = generateTestPolynomial( order, N[order], t0, tau )
            f = PairedPolynomialFilter(order, tau, theta)
            (times, truth, observations, noise) = generateTestData(order, N[order], 0.0, Y[0:order+1], tau, sigma=R)
            testData.putArray(case, 'times', times)
            testData.putArray(case, 'observations', observations)
            expected = zeros([N[order], order+1]) 
            vdiags = zeros([N[order], order+1]) 
            lastV = ones([order+1, order+1])
            for j in range(0,nS) :
                Zstar = f.predict(times[j][0])
                e = observations[j] - Zstar[0]
                f.update(times[j][0], Zstar, e)
#                 print(f.getN(), N[order], nS, A2S(diag(f.getVRF())), A2S(diag(lastV)-diag(f.getVRF())))
                expected[j,:] = f.getState();
                vdiags[j,:] = diag(f.getVRF())
                if (f.getStatus() == FilterStatus.RUNNING) : 
                    self.assertFalse(array_equal(lastV, f.getVRF()))
                lastV = f.getVRF()
            for j in range(nS,N[order]) :
                Zstar = f.predict(times[j][0])
                e = observations[j] - Zstar[0]
                f.update(times[j][0], Zstar, e)
#                 print(f.getN(), N[order], nS, A2S(diag(f.getVRF())), A2S(diag(lastV)-diag(f.getVRF())))
                expected[j,:] = f.getState();
                vdiags[j,:] = diag(f.getVRF())
                self.assertTrue(array_equal(lastV, f.getVRF()))
                
            testData.putArray(case, 'expected', expected)
            testData.putArray(case, 'vdiags', vdiags)
       
    def xstep0Generate(self):
        testData = TestData('testPair.nc', 'w');
        self.generateStates(testData)
        testData.close()
       

    @testcase
    def step2CheckStates(self):
        '''@testData : TestData'''
        '''@states : Group'''
        '''@caseGroup : Group'''
        '''@matches : List[str]'''
        '''@order : int'''
        '''@tau : float'''
        '''@theta : float'''
        '''@nS : int'''
        '''@N : int'''
        '''@times : array'''
        '''@observations : array'''
        '''@expectedStates : array'''
        '''@expectedVdiag : array'''
        '''@actual : array'''
        '''@vdiags : array'''
        '''@f : PairedPolynomialFilter'''
        
        '''@Zstar : array'''
        '''@diff : array'''
        '''@i : int'''
        '''@j : int'''
        '''@e : float'''
#         print("test2CheckStates")
        assert_clear()
        testData = TestData('testPair.nc')
        states = testData.getGroup('States')
        matches = testData.getMatchingGroups('States_Case_')
        assert_not_empty(matches)
        for i in range(0, len(matches)) :
            caseGroup = testData.getGroup(matches[i])
            order = testData.getInteger(caseGroup, 'order')
            tau = testData.getScalar(caseGroup, 'tau')
            theta = testData.getScalar(caseGroup, 'theta')
            nS = testData.getInteger(caseGroup, 'nS')
            N = testData.getInteger(caseGroup, 'N')
            times = testData.getArray(caseGroup, 'times')
            observations = testData.getArray(caseGroup, 'observations')
            expectedStates = testData.getArray(caseGroup, 'expected')
            expectedVdiag = testData.getArray(caseGroup, 'vdiags')

            
            f = PairedPolynomialFilter(order, tau, theta)
#             print(order, tau, theta, nS, f.threshold)
            actual = zeros([N, order+1]) 
            vdiags = zeros([N, order+1]) 
            for j in range(0,N) : 
                Zstar = f.predict(times[j,0])
                e = observations[j] - Zstar[0]
                f.update(times[j,0], Zstar, e)
                actual[j,:] = transpose(f.getState())
                vdiags[j,:] = transpose(diag(f.getVRF()))
                

            assert_allclose( actual, expectedStates)
            assert_allclose( vdiags, expectedVdiag)
        testData.close()
        assert_report('Pair_test/test2CheckStates', -1)
        
    @testcase
    def step9Coverage(self):
        '''@f : PairedPolynomialFilter'''
        '''@t : int'''
        '''@Zstar : array'''
        f = PairedPolynomialFilter(0, 1.0, 0.5)
        f.start(0.0, array([10]))
        self.assertEqual(0.0, f.getTime())
        assert_allclose( f.getState(), array([10]))
        self.assertFalse( f.isFading() )
        for t in range(1, 1+3) :
            Zstar = f.predict(t)
            f.update(t, Zstar, 0.0)
            self.assertFalse( f.isFading() )
        Zstar = f.predict(4)
        f.update(4, Zstar, 0.0)
        self.assertTrue( f.isFading() )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()