'''
Created on Feb 23, 2019

@author: NOOK

 netCDF4 Visual Studio https://www.unidata.ucar.edu/software/netcdf/docs/winbin.html
 C:\Program Files\netCDF 4.6.3
'''
import unittest
from netCDF4 import Dataset
from TestUtilities import *
from numpy import arange, array2string, cov, zeros, mean, std, var, diag,\
    transpose, concatenate
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal
from numpy.testing import assert_allclose
from math import sqrt, sin
from runstats import Statistics
from scipy.stats._continuous_distns import chi2

from polynomialfiltering.components.FixedMemoryPolynomialFilter import FixedMemoryFilter;

from TestSuite import testDataPath;
from TestData import TestData
from polynomialfiltering.PythonUtilities import ignore, testcase, testmethod, testclass, testclassmethod
from polynomialfiltering.PythonUtilities import assert_not_empty


class FixedMemoryFilter_test(unittest.TestCase):
    '''@testData : TestData'''
    
    @classmethod
    def setUpClass(self):
        self.Y0 = array([1e4, 1e3, 1e2, 1e1, 1e0, 1e-1]);
 
    @classmethod
    def tearDownClass(self):
        pass
 
     
 
    @testmethod
    def executeEstimatedState(self, setup : array, data : array ) -> array:
        '''@order : int'''
        '''@window : int'''
        '''@M : int'''
        '''@iCheck : int'''
        '''@times : array'''
        '''@observations : array'''
        '''@fixed : FixedMemoryFilter'''
        '''@i : int'''
        order = int(setup[0]);
        window = int(setup[1]);
        M = int(setup[2]);
        iCheck = int(setup[3]);
        times = data[:,0:1];
        observations = data[:,1:2];
        fixed = FixedMemoryFilter(order, window);
        for i in range(0,M) :
            fixed.add(times[i], observations[i]);
        return fixed.transitionState(times[iCheck]);
                 
                 
    def generatePerfect(self, testData : TestData ) -> None:
        setup = array([None, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(2,6):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=0.0)
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup( 'testPerfect_%d' % order );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
#             print('setup ',setup)
#             print('data ',data)
             
            expected = self.executeEstimatedState(setup, data);
#             print(order, expected)
             
            testData.putArray(group, 'expected', expected);
            assert_allclose( expected, truth[11,:], atol=0, rtol=1e-3 )
 
    def generateNoisy(self, testData : TestData ) -> None:
        setup = array([None, 11, 12, 11]);
        tau = 0.1;
        N = 25;
        for order in range(2,6):
            setup[0] = order; 
            (times, truth, observations, noise) = generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=1.0)
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup('testNoisy_%d' % order );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
             
            expected = self.executeEstimatedState(setup, data);
             
            testData.putArray(group, 'expected', expected);
            #assert_allclose( expected, truth[11,:], atol=0, rtol=1e-2 )
 
     
    def generateMidpoints(self, testData : TestData ) -> None:
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for iCheck in range(offset, M) :
            setup = array([order, window, M, iCheck]);
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
             
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup( 'testMidpoints_%d' % iCheck );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
             
            expected = self.executeEstimatedState(setup, data);
             
            testData.putArray(group, 'expected', expected);
            assert_allclose( truth[iCheck,:], expected );
             
    @testmethod
    def executeVRF(self, setup : array, data : array ) -> array:
        '''@order : int'''
        '''@window : int'''
        '''@M : int'''
        '''@iCheck : int'''
        '''@times : array'''
        '''@observations : array'''
        '''@fixed : FixedMemoryFilter'''
        '''@i : int'''
        order = int(setup[0]);
        window = int(setup[1]);
        M = int(setup[2]);
        iCheck = int(setup[3]);
        times = data[:,0:1];
        observations = data[:,1:2];
        fixed = FixedMemoryFilter(order, window);
        for i in range(0,M) :
            fixed.add(times[i], observations[i]);
        return fixed.getVRF();
                 
    def generateVRF(self, testData : TestData ) -> None:
        tau = 0.1;
        N = 25;
        window = 11;
        M = 12; # number of points to input
        iCheck = M-1;
        for order in range(2,6) :
            setup = array([order, window, M, iCheck]);
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=0.0)
             
            data = concatenate([times, observations], axis=1);
            group = testData.createTestGroup('testVRF_%d' % order );
            testData.putArray(group, 'setup', setup);
            testData.putArray(group, 'data', data);
             
            expected = self.executeVRF(setup, data);
             
            testData.putArray(group, 'expected', expected);
         
         
    def xtestVRFStatistics(self):
        '''
         This extended numeric test validates the computed VRF matrix
         against the actual residuals for a large sample of filter runs.
         N=1000, K=5000, 492.609 seconds
        [     0.998          1          1          1          1          1          1          1          1]        
        '''
        tau = 0.1;
        N = 1000;
        order = 2;
        window = 51;
        M = window; # number of points for initial input
        setup = array([order, window, M]);
        K = 5000;
        C = zeros([K,(order+1)**2])
        for k in range(0,K) :
            fixed = FixedMemoryFilter(order, window);
            (times, truth, observations, noise) = generateTestData(fixed.order, N, 0.0, self.Y0[0:fixed.order+1], tau, sigma=1.0)
            for i in range(0,window) :
                fixed.add(times[i], observations[i]);
            results = zeros([N-window, order+1]);
            for i in range(window, N) :
                fixed.add(times[i], observations[i]);
                results[i-window,:] = fixed.getState() - truth[i,:];
            c = cov(results,rowvar=False);
            C[k,:] = c.flatten();
            V = fixed.getCovariance();
             
        E = mean(C,axis=0) / V.flatten()
        print( A2S( E ) );
        assert_allclose( E, ones([(order+1)**2]), atol=1e-2 )
         
 
    def test0Generate(self):
        testData = TestData('FixedMemoryFiltering.nc', 'w')
        
        self.generatePerfect(testData)
        self.generateNoisy(testData)
        self.generateMidpoints(testData)
        self.generateVRF(testData)
        
        testData.close()

    @testcase
    def test1CheckPerfect(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@order : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testPerfect_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0]) 
            data = testData.getArray(group, 'data');
            actual = self.executeEstimatedState(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()

    @testcase
    def test1CheckNoisy(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@order : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testNoisy_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0]) 
            data = testData.getArray(group, 'data');
            actual = self.executeEstimatedState(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()

    @testcase
    def test1CheckMidpoints(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@M : int'''
        '''@window : int'''
        '''@iCheck : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@offset : int'''
        '''@order : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testMidpoints_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0])
            window = int(setup[1])
            M = int(setup[2])
            iCheck = int(setup[3])
            data = testData.getArray(group, 'data');
            actual = self.executeEstimatedState(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()
    
    @testcase
    def test1CheckVrfs(self):
        '''@matches : List[str]'''
        '''@tau : float'''
        '''@N : int'''
        '''@M : int'''
        '''@window : int'''
        '''@iCheck : int'''
        '''@i : int'''
        '''@group : Group'''
        '''@setup : vector'''
        '''@order : int'''
        '''@offset : int'''
        '''@data : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@testData : TestData'''
        
        testData = TestData('FixedMemoryFiltering.nc')
        matches = testData.getMatchingGroups('testVRF_')
        assert_not_empty(matches)
        tau = 0.1;
        N = 25;
        order = 2;
        window = 11;
        M = 12; # number of points to input
        offset = M - window;
        for i in range(0, len(matches)) :
            group = testData.getGroup(matches[i])
            setup = testData.getArray(group, 'setup')
            order = int(setup[0])
            window = int(setup[1])
            M = int(setup[2])
            iCheck = int(setup[3])
            data = testData.getArray(group, 'data');
            actual = self.executeVRF(setup, data);
            expected = testData.getArray(group, 'expected');
            assert_allclose( expected, actual )
        testData.close()

    @testclass
    class TestFixedMemoryFilter(FixedMemoryFilter): 
        @testclassmethod
        def __init__(self, order : int):
            super().__init__(order)
        
        @testclassmethod
        def getOrder(self) -> int:
            return self.order
        
        @testclassmethod
        def getL(self) -> int:
            return self.L
        

    @testcase
    def test9Regresssion(self):
        '''@fixed : TestFixedMemoryFilter'''
        fixed = self.TestFixedMemoryFilter(4)
        self.assertEqual(fixed.getOrder(), 4)
        self.assertEqual(fixed.getL(), 51)
           
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()