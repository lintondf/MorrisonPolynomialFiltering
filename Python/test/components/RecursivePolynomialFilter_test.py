'''
Created on Apr 19, 2019

@author: NOOK
'''
from abc import ABC, abstractmethod
import unittest

from numpy import array as vector
from numpy import array, ones, zeros, concatenate, transpose, sqrt
from numpy import cov
from TestUtilities import assert_allclose, assert_almost_equal, assert_array_less

from TestSuite import TestCaseBase
from TestData import TestData
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S, assert_report, assert_clear
from polynomialfiltering.Main import FilterStatus
from polynomialfiltering.PythonUtilities import assert_not_empty
from polynomialfiltering.PythonUtilities import ignore, testcase
from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.filters.RecursivePolynomialFilter import RecursivePolynomialFilter, ICore


# from numpy.linalg import inv
# from numpy.random import randn
# from netCDF4 import Dataset
# from TestUtilities import *
# from TestSuite import testDataPath;
class RecursivePolynomialFilter_test(TestCaseBase):

    """ PurePredictCore ignores observations producing a results solely from the state transition update"""
    @testclass
    class PurePredictCore(ICore): 
        '''@order : int'''
        
        @testclassmethod
        def __init__(self, order : int):
            self.order = order;
            pass
        
        @testclassmethod
        def getSamplesToStart(self) -> int:
            return 1
        
        @testclassmethod
        def getGamma(self, t : float, dtau : float) -> vector:
            '''@g : vector'''
            g = zeros([self.order+1])
            return g
        
        @testclassmethod
        def getVRF(self, n : int) -> array:
            '''@Z  : array'''
            Z = zeros([self.order+1, self.order+1])
            return Z
        
        @testclassmethod
        def getFirstVRF(self, n : int) -> float:
            return 0.0;
    
        @testclassmethod
        def getLastVRF(self, n : int) -> float:
            return 0.0;
        
       
    """ PureObservationCore ignores predictions producing a results solely from the observation update"""
    @testclass
    class PureObservationCore(ICore): 
        '''@order : int'''
        
        @testclassmethod
        def __init__(self, order : int):
            self.order = order;
            pass
        
        @testclassmethod
        def getSamplesToStart(self) -> int:
            return 2
        
        @testclassmethod
        def getGamma(self, t : float, dtau : float) -> vector:
            '''@g : vector'''
            g = 1.0+zeros([self.order+1])
            return g
        
        @testclassmethod
        def getVRF(self, n : int) -> array:
            '''@Z  : array'''
            Z = zeros([self.order+1, self.order+1])
            return Z
        
        @testclassmethod
        def getFirstVRF(self, n : int) -> float:
            return 0.0;
    
        @testclassmethod
        def getLastVRF(self, n : int) -> float:
            return 0.0;
               
       
    Y0 = array([1e4, -5e3, +1e3, -5e2, +1e2, -5e1]);

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def step0Generate(self):
        testData = TestData('testRecursivePolynomialFilter.nc', 'w');
        
        N = 5;
        iTest = 0;
        for order in range(5,5+1) :
            for tau in [0.1, 1, 10] :
                group = testData.createTestGroup('testPurePredict_%d' % iTest );
                iTest += 1;
                (times, truth, observations, noise) = \
                    generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=sqrt(1.0))

                setup = array([N, order, tau])
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'times', times);
                writeTestVariable(group, 'truth', truth);
                writeTestVariable(group, 'observations', observations);

                actual = zeros([N, order+1]);
                actual[0,:] = truth[0,:];

                core = self.PurePredictCore(order)
                f = RecursivePolynomialFilter(order, tau, core );
                f.start(times[0], truth[0,:]);
                for i in range(1,N) :
                    Zstar = f.predict(times[i])
                    assert_allclose( f._denormalizeState(Zstar), truth[i,:], atol=1e-6 )
                    e = observations[i] - Zstar[0]
                    f.update(times[i], Zstar, e)
                    assert_allclose( f.getState(), truth[i,:], atol=1e-6 )
                    actual[i,:] = f.getState();
                    V = f.getVRF();
                    assert(f.getN() == i );    
                    assert_almost_equal(V, zeros([order+1, order+1]))

                writeTestVariable(group, 'expected', actual);
        iTest = 0;
        for order in range(5,5+1) :
            for tau in [0.1, 1, 10] :
                group = testData.createTestGroup('testPureObservation_%d' % iTest );
                iTest += 1;
                (times, truth, observations, noise) = \
                    generateTestData(order, N, 0.0, self.Y0[0:order+1], tau, sigma=sqrt(1.0))

                setup = array([N, order, tau])
                
                writeTestVariable(group, 'setup', setup);
                writeTestVariable(group, 'times', times);
                writeTestVariable(group, 'truth', truth);
                writeTestVariable(group, 'observations', observations);

                es = zeros([N, 1]);
                Zstars = zeros([N, order+1]);
                innovations = zeros([N, order+1]);
                actual = zeros([N, order+1]);
                actual[0,:] = truth[0,:];

                core = self.PureObservationCore(order)
                f = RecursivePolynomialFilter(order, tau, core );
                f.start(times[0], truth[0,:]);
                for i in range(1,N) :
                    Zstar = f.predict(times[i])
                    e = observations[i] - Zstar[0]
                    
                    Zstars[i,:] = transpose(Zstar)
                    es[i] = e;
                    innovations[i,:] = transpose(f.update(times[i], Zstar, e))
                    actual[i,:] = f.getState();
                    V = f.getVRF();

                writeTestVariable(group, 'Zstars', Zstars);
                writeTestVariable(group, 'es', es);
                writeTestVariable(group, 'innovations', innovations);
                writeTestVariable(group, 'expected', actual);
        testData.close()
        
        
    @testcase
    def step1PurePredict(self) -> None: 
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@iMatch : int'''
        '''@N : int'''
        '''@order : int'''
        '''@tau : float'''
        '''@setup : array'''
        '''@times : array'''
        '''@truth : array'''
        '''@observations : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@core : ICore'''
        '''@f : RecursivePolynomialFilter'''
        '''@Zstar : vector'''
        '''@e : float'''
        '''@V : array'''
        '''@i : int'''
        
        assert_clear()
        testData = TestData('testRecursivePolynomialFilter.nc')
        matches = testData.getMatchingGroups('testPurePredict_')
        assert_not_empty(matches)
        for iMatch in range(0, len(matches)) :
            setup = testData.getGroupVariable(matches[iMatch], 'setup')
            times = testData.getGroupVariable(matches[iMatch], 'times')
            truth = testData.getGroupVariable(matches[iMatch], 'truth')
            observations = testData.getGroupVariable(matches[iMatch], 'observations')
            
            N = int(setup[0])
            order = int(setup[1])
            tau = setup[2]
            
            actual = zeros([N, order+1]);
            actual[0,:] = truth[0,:];

            core = self.PurePredictCore(order)
            f = RecursivePolynomialFilter(order, tau, core );
            f.start(times[0], truth[0,:]);
            for i in range(1,N) :
                Zstar = f.predict(times[i])
                e = observations[i] - Zstar[0]
                f.update(times[i], Zstar, e)
                actual[i,:] = transpose(f.getState());
                V = f.getVRF();
                assert(f.getN() == i );    
                assert_almost_equal(V, zeros([order+1, order+1]))
            
            expected = testData.getGroupVariable(matches[iMatch], 'expected')
            assert_almost_equal( actual, expected )
        assert_report("RecursivePolynomialFilter_test/test1PurePredict", -1)     
        testData.close()

    @testcase
    def step1PureObservation(self) -> None: 
        '''@testData : TestData'''
        '''@matches : List[str]'''
        '''@iMatch : int'''
        '''@N : int'''
        '''@order : int'''
        '''@tau : float'''
        '''@setup : array'''
        '''@times : array'''
        '''@truth : array'''
        '''@observations : array'''
        '''@es : array'''
        '''@Zstars : array'''
        '''@innovation : array'''
        '''@innovations : array'''
        '''@actual : array'''
        '''@expected : array'''
        '''@core : ICore'''
        '''@f : RecursivePolynomialFilter'''
        '''@Zstar : vector'''
        '''@e : float'''
        '''@V : array'''
        '''@i : int'''
        
        assert_clear()
        testData = TestData('testRecursivePolynomialFilter.nc')
        matches = testData.getMatchingGroups('testPureObservation_')
        assert_not_empty(matches)
        for iMatch in range(0, len(matches)) :
            setup = testData.getGroupVariable(matches[iMatch], 'setup')
            times = testData.getGroupVariable(matches[iMatch], 'times')
            truth = testData.getGroupVariable(matches[iMatch], 'truth')
            observations = testData.getGroupVariable(matches[iMatch], 'observations')
            
            N = int(setup[0])
            order = int(setup[1])
            tau = setup[2]
            
            es = testData.getGroupVariable(matches[iMatch], 'es')
            Zstars = testData.getGroupVariable(matches[iMatch], 'Zstars')
            innovations = testData.getGroupVariable(matches[iMatch], 'innovations')
            expected = testData.getGroupVariable(matches[iMatch], 'expected')
            actual = zeros([N, order+1]);
            actual[0,:] = truth[0,:];

            core = self.PureObservationCore(order)
            f = RecursivePolynomialFilter(order, tau, core );
            f.start(times[0], truth[0,:]);
            for i in range(1,N) :
                Zstar = f.predict(times[i])
                assert_almost_equal(Zstar, transpose(Zstars[i,:]))
                e = observations[i] - Zstar[0]
                
                assert_almost_equal(e, es[i])
                innovation = f.update(times[i], Zstar, e)
                assert_almost_equal(innovation, transpose(innovations[i,:]))
                actual[i,:] = transpose(f.getState());
                V = f.getVRF();
                assert(f.getN() == i );    
                assert_almost_equal(V, zeros([order+1, order+1]))
            
            assert_almost_equal( actual, expected )
        assert_report("RecursivePolynomialFilter_test/test1PureObservation", -1)       
        testData.close()

    @testcase
    def step9Coverage(self):
        '''@core : ICore'''
        '''@f : RecursivePolynomialFilter'''
        '''@g : RecursivePolynomialFilter'''
        '''@name : str'''
        '''@Zstar : vector'''
        '''@I : array'''
        assert_clear()
        core = self.PureObservationCore(2)
        f = RecursivePolynomialFilter(2, 1.0, core );
        self.assertEqual(2, f.getOrder())
        self.assertEqual(1.0, f.getTau())
        f.setName('hello')
        name = f.getName()
        self.assertEqual(f.getStatus(), FilterStatus.IDLE);
        f.start(0.0, array([1.0,2.0,3.0]))
        self.assertEqual(f.getStatus(), FilterStatus.IDLE);
        self.assertEqual(f.getFirstVRF(), 0.0)
        self.assertEqual(f.getLastVRF(), 0.0)
        Zstar = f.predict(1.0)
        f.update(1.0, Zstar, 0.0)
        self.assertEqual(f.getStatus(), FilterStatus.INITIALIZING);
        Zstar = f.predict(2.0)
        f.update(2.0, Zstar, 0.0)
        self.assertEqual(f.getStatus(), FilterStatus.RUNNING);
        assert_almost_equal(f.getState(), array([11.0, 8.0, 3.0]))
        assert_almost_equal(f.transitionState(4.0), array([33.0, 14.0, 3.0]))
        self.assertEqual(2, f.getN())
        self.assertEqual(RecursivePolynomialFilter.effectiveTheta(2, 0), 0)
        assert_almost_equal(RecursivePolynomialFilter.effectiveTheta(2, 10), 0.56673)
        
        g = RecursivePolynomialFilter(2, 1.0, core );
        g.copyState(f)
        assert_almost_equal(g.getState(), array([11.0, 8.0, 3.0]))
        assert_report("RecursivePolynomialFilter_test/test9Coverage", -1)
        
 
if __name__ == "__main__":
    unittest.main()