'''
Created on Apr 19, 2019

@author: NOOK
'''
import unittest

from abc import ABC, abstractmethod

from numpy import array, ones, zeros, concatenate
from numpy import array as vector

from numpy import cov
from numpy.linalg import inv
from numpy.random import randn
from numpy.testing import assert_almost_equal, assert_allclose
from netCDF4 import Dataset
from TestUtilities import *
from TestSuite import testDataPath;
from polynomialfiltering.PythonUtilities import ignore, testcase
from TestData import TestData

from polynomialfiltering.PythonUtilities import ignore, testcase, testclass, testclassmethod
from polynomialfiltering.PythonUtilities import assert_not_empty


from polynomialfiltering.components.RecursivePolynomialFilter import RecursivePolynomialFilter, ICore

@testclass
class PurePredictCore(ICore): 
    
    '''@order : int'''
    
    @testclassmethod
    def __init__(self, order : int):
        self.order = order;
        pass
    
    @testclassmethod
    def getGamma(self, t : float, dtau : float) -> vector:
        '''@g : vector'''
        g = zeros([self.order+1])
        return g
    
    @testclassmethod
    def getVRF(self, n : int) -> array:
        return zeros([self.order+1, self.order+1])
    
    @testclassmethod
    def getFirstVRF(self, n : int) -> float:
        return 0.0;

    @testclassmethod
    def getLastVRF(self, n : int) -> float:
        return 0.0;
    
    @testclassmethod
    def getDiagonalVRF(self, n : int) -> array:
        return zeros([self.order+1, self.order+1])
       
       
class RecursivePolynomialFilter_test(unittest.TestCase):

#     Y0 = array([1e4, -5e3, +1e3, -5e2, +1e2, -5e1]);

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test0Generate(self):
        path = testDataPath('testRecursivePolynomialFilter.nc');
#         print("Writing to: ", path)
        cdf = Dataset(path, "w", format="NETCDF4");
        
        N = 100;
        iTest = 0;
        for order in range(5,5+1) :
            for tau in [0.1, 1, 10] :
                group = createTestGroup(cdf, 'testPurePredict_%d' % iTest );
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

                core = PurePredictCore(order)
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

    @testcase
    def test1PurePredict(self) -> None: 
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

            core = PurePredictCore(order)
            f = RecursivePolynomialFilter(order, tau, core );
            f.start(times[0], truth[0,:]);
            for i in range(1,N) :
                Zstar = f.predict(times[i])
                e = observations[i] - Zstar[0]
                f.update(times[i], Zstar, e)
                actual[i,:] = f.getState();
                V = f.getVRF();
                assert(f.getN() == i );    
                assert_almost_equal(V, zeros([order+1, order+1]))
            
            expected = testData.getGroupVariable(matches[iMatch], 'expected')
            assert_almost_equal( actual, expected )
            
        testData.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test0Generate']
    unittest.main()